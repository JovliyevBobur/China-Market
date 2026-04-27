"""
📋 Order Repository Module

Repository for order-related database operations.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Sequence
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.config.constants import OrderStatus, PaymentStatus
from app.database.models import Order, OrderItem

from .base_repo import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Order repository with specialized queries.
    """
    
    model = Order
    
    async def get_by_id_with_items(self, id: int) -> Optional[Order]:
        """
        Get order with all items loaded.
        
        Args:
            id: Order ID
        
        Returns:
            Order with items or None
        """
        result = await self.session.execute(
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.user),
                selectinload(Order.payments),
            )
            .where(Order.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_order_number(self, order_number: str) -> Optional[Order]:
        """
        Get order by order number.
        
        Args:
            order_number: Order number
        
        Returns:
            Order or None
        """
        result = await self.session.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()
    
    async def get_user_orders(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
        status: Optional[OrderStatus] = None,
    ) -> Sequence[Order]:
        """
        Get orders for user.
        
        Args:
            user_id: User ID
            limit: Maximum number of records
            offset: Number of records to skip
            status: Filter by status
        
        Returns:
            Sequence of orders
        """
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
        )
        
        if status:
            stmt = stmt.where(Order.status == status)
        
        stmt = stmt.order_by(Order.created_at.desc())
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_seller_orders(
        self,
        seller_id: int,
        limit: int = 50,
        offset: int = 0,
        status: Optional[OrderStatus] = None,
    ) -> Sequence[Order]:
        """
        Get orders containing seller's products.
        
        Args:
            seller_id: Seller ID
            limit: Maximum number of records
            offset: Number of records to skip
            status: Filter by status
        
        Returns:
            Sequence of orders
        """
        stmt = (
            select(Order)
            .join(OrderItem)
            .options(selectinload(Order.items))
            .where(OrderItem.seller_id == seller_id)
            .distinct()
        )
        
        if status:
            stmt = stmt.where(Order.status == status)
        
        stmt = stmt.order_by(Order.created_at.desc())
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create_order(
        self,
        user_id: int,
        items: list[dict],
        customer_name: str,
        customer_phone: str,
        delivery_type: str,
        payment_method: str,
        delivery_address: Optional[str] = None,
        delivery_city: Optional[str] = None,
        customer_notes: Optional[str] = None,
        promo_code: Optional[str] = None,
    ) -> Order:
        """
        Create new order with items.
        
        Args:
            user_id: User ID
            items: List of order items data
            customer_name: Customer name
            customer_phone: Customer phone
            delivery_type: Delivery type
            payment_method: Payment method
            delivery_address: Delivery address
            delivery_city: Delivery city
            customer_notes: Customer notes
            promo_code: Applied promo code
        
        Returns:
            Created order
        """
        # Generate order number
        order_number = self._generate_order_number()
        
        # Calculate totals
        subtotal = sum(
            Decimal(str(item["unit_price"])) * item["quantity"]
            for item in items
        )
        discount_amount = Decimal(0)
        delivery_fee = Decimal(0)  # Calculate based on delivery_type
        total_amount = subtotal - discount_amount + delivery_fee
        
        # Create order
        order = Order(
            user_id=user_id,
            order_number=order_number,
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_type=delivery_type,
            payment_method=payment_method,
            delivery_address=delivery_address,
            delivery_city=delivery_city,
            customer_notes=customer_notes,
            promo_code=promo_code,
            subtotal=subtotal,
            discount_amount=discount_amount,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
        )
        
        self.session.add(order)
        await self.session.flush()
        
        # Create order items
        for item_data in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                seller_id=item_data["seller_id"],
                product_name=item_data["product_name"],
                product_sku=item_data.get("product_sku"),
                product_image=item_data.get("product_image"),
                unit_price=Decimal(str(item_data["unit_price"])),
                quantity=item_data["quantity"],
                discount_amount=Decimal(str(item_data.get("discount_amount", 0))),
                total_price=Decimal(str(item_data["unit_price"])) * item_data["quantity"],
            )
            self.session.add(order_item)
        
        await self.session.flush()
        await self.session.refresh(order)
        
        return order
    
    def _generate_order_number(self) -> str:
        """Generate unique order number."""
        now = datetime.utcnow()
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"ORD-{now.strftime('%Y%m%d')}-{unique_id}"
    
    async def update_status(
        self,
        order_id: int,
        status: OrderStatus,
    ) -> Optional[Order]:
        """
        Update order status.
        
        Args:
            order_id: Order ID
            status: New status
        
        Returns:
            Updated order or None
        """
        order = await self.get_by_id(order_id)
        if order:
            order.set_status(status)
            await self.session.flush()
        return order
    
    async def cancel_order(
        self,
        order_id: int,
        reason: str,
        cancelled_by: str = "user",
    ) -> Optional[Order]:
        """
        Cancel order.
        
        Args:
            order_id: Order ID
            reason: Cancellation reason
            cancelled_by: Who cancelled (user/admin/system)
        
        Returns:
            Cancelled order or None
        """
        order = await self.get_by_id(order_id)
        if order and order.can_cancel:
            order.cancel(reason, cancelled_by)
            await self.session.flush()
            return order
        return None
    
    async def mark_paid(
        self,
        order_id: int,
    ) -> Optional[Order]:
        """
        Mark order as paid.
        
        Args:
            order_id: Order ID
        
        Returns:
            Updated order or None
        """
        order = await self.get_by_id(order_id)
        if order:
            order.mark_paid()
            await self.session.flush()
        return order
    
    async def count_by_status(self, status: OrderStatus) -> int:
        """
        Count orders by status.
        
        Args:
            status: Order status
        
        Returns:
            Order count
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(Order)
            .where(Order.status == status)
        )
        return result.scalar_one()
    
    async def count_user_orders(self, user_id: int) -> int:
        """
        Count user's orders.
        
        Args:
            user_id: User ID
        
        Returns:
            Order count
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(Order)
            .where(Order.user_id == user_id)
        )
        return result.scalar_one()
    
    async def get_expired_pending_orders(
        self,
        expire_minutes: int = 60,
    ) -> Sequence[Order]:
        """
        Get pending orders that have expired.
        
        Args:
            expire_minutes: Minutes after which order expires
        
        Returns:
            Sequence of expired orders
        """
        expire_time = datetime.utcnow() - timedelta(minutes=expire_minutes)
        
        result = await self.session.execute(
            select(Order)
            .where(
                Order.status == OrderStatus.PENDING,
                Order.payment_status == PaymentStatus.PENDING,
                Order.created_at < expire_time,
            )
        )
        return result.scalars().all()
    
    async def get_daily_stats(self, date: Optional[datetime] = None) -> dict:
        """
        Get daily order statistics.
        
        Args:
            date: Date for stats (default: today)
        
        Returns:
            Dictionary with stats
        """
        if date is None:
            date = datetime.utcnow().date()
        
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        
        # Total orders
        total_orders = await self.session.execute(
            select(func.count())
            .select_from(Order)
            .where(
                Order.created_at >= start,
                Order.created_at <= end,
            )
        )
        
        # Total revenue
        total_revenue = await self.session.execute(
            select(func.sum(Order.total_amount))
            .where(
                Order.created_at >= start,
                Order.created_at <= end,
                Order.payment_status == PaymentStatus.COMPLETED,
            )
        )
        
        # Completed orders
        completed_orders = await self.session.execute(
            select(func.count())
            .select_from(Order)
            .where(
                Order.created_at >= start,
                Order.created_at <= end,
                Order.status == OrderStatus.COMPLETED,
            )
        )
        
        return {
            "date": date,
            "total_orders": total_orders.scalar_one(),
            "total_revenue": total_revenue.scalar_one() or Decimal(0),
            "completed_orders": completed_orders.scalar_one(),
        }
