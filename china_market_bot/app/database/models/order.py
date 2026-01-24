"""
📋 Order Model Module

Order and OrderItem database models.
"""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.constants import DeliveryType, OrderStatus, PaymentMethod, PaymentStatus

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .payment import Payment
    from .product import Product
    from .user import User


class Order(Base, IDMixin, TimestampMixin):
    """
    Order model representing user orders.
    
    Contains order details, status, delivery info, and payment info.
    """
    
    __tablename__ = "orders"
    
    # User relationship
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Reference to user",
    )
    
    # Order number
    order_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Human-readable order number",
    )
    
    # Status
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True,
        comment="Order status",
    )
    
    # Pricing
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Subtotal before discounts and delivery",
    )
    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        default=Decimal(0),
        nullable=False,
        comment="Total discount amount",
    )
    delivery_fee: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        default=Decimal(0),
        nullable=False,
        comment="Delivery fee",
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Total order amount",
    )
    
    # Promo code
    promo_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Applied promo code",
    )
    
    # Customer Info
    customer_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Customer full name",
    )
    customer_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Customer phone number",
    )
    customer_email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Customer email",
    )
    
    # Delivery Info
    delivery_type: Mapped[DeliveryType] = mapped_column(
        Enum(DeliveryType, name="delivery_type"),
        default=DeliveryType.STANDARD,
        nullable=False,
        comment="Delivery type",
    )
    delivery_address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Delivery address",
    )
    delivery_city: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Delivery city",
    )
    delivery_region: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Delivery region",
    )
    delivery_postal_code: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Postal code",
    )
    
    # Delivery dates
    estimated_delivery: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Estimated delivery date",
    )
    shipped_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When order was shipped",
    )
    delivered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When order was delivered",
    )
    
    # Tracking
    tracking_number: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Shipping tracking number",
    )
    
    # Payment
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method"),
        default=PaymentMethod.CASH,
        nullable=False,
        comment="Payment method",
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="order_payment_status"),
        default=PaymentStatus.PENDING,
        nullable=False,
        comment="Payment status",
    )
    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When order was paid",
    )
    
    # Notes
    customer_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Customer notes",
    )
    admin_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Admin/seller notes",
    )
    
    # Cancellation
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When order was cancelled",
    )
    cancellation_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Cancellation reason",
    )
    cancelled_by: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Who cancelled (user/admin/system)",
    )
    
    # Refund
    is_refunded: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is order refunded",
    )
    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        default=Decimal(0),
        nullable=False,
        comment="Refund amount",
    )
    refunded_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When order was refunded",
    )
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="orders",
        lazy="selectin",
    )
    
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="order",
        lazy="selectin",
    )
    
    # Properties
    @property
    def item_count(self) -> int:
        """Get number of unique items."""
        return len(self.items)
    
    @property
    def total_quantity(self) -> int:
        """Get total quantity of all items."""
        return sum(item.quantity for item in self.items)
    
    @property
    def is_paid(self) -> bool:
        """Check if order is paid."""
        return self.payment_status == PaymentStatus.COMPLETED
    
    @property
    def can_cancel(self) -> bool:
        """Check if order can be cancelled."""
        return self.status in (OrderStatus.PENDING, OrderStatus.CONFIRMED)
    
    @property
    def can_refund(self) -> bool:
        """Check if order can be refunded."""
        return (
            self.is_paid
            and not self.is_refunded
            and self.status not in (OrderStatus.CANCELLED,)
        )
    
    def set_status(self, status: OrderStatus) -> None:
        """Update order status and related timestamps."""
        self.status = status
        
        if status == OrderStatus.SHIPPED:
            self.shipped_at = datetime.utcnow()
        elif status == OrderStatus.DELIVERED:
            self.delivered_at = datetime.utcnow()
        elif status == OrderStatus.CANCELLED:
            self.cancelled_at = datetime.utcnow()
    
    def mark_paid(self) -> None:
        """Mark order as paid."""
        self.payment_status = PaymentStatus.COMPLETED
        self.paid_at = datetime.utcnow()
        if self.status == OrderStatus.PENDING:
            self.status = OrderStatus.CONFIRMED
    
    def cancel(self, reason: str, cancelled_by: str = "user") -> None:
        """Cancel order."""
        self.status = OrderStatus.CANCELLED
        self.cancelled_at = datetime.utcnow()
        self.cancellation_reason = reason
        self.cancelled_by = cancelled_by


class OrderItem(Base, IDMixin, TimestampMixin):
    """
    Order item model representing individual items in an order.
    """
    
    __tablename__ = "order_items"
    
    # Relationships
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to order",
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Reference to product",
    )
    seller_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Seller ID (denormalized)",
    )
    
    # Product snapshot
    product_name: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        comment="Product name at order time",
    )
    product_sku: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Product SKU at order time",
    )
    product_image: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Product image URL at order time",
    )
    
    # Pricing
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Unit price at order time",
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Quantity ordered",
    )
    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        default=Decimal(0),
        nullable=False,
        comment="Discount amount per unit",
    )
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Total price for this item",
    )
    
    # Relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items",
        lazy="selectin",
    )
    
    product: Mapped[Optional["Product"]] = relationship(
        "Product",
        back_populates="order_items",
        lazy="selectin",
    )
    
    # Properties
    @property
    def subtotal(self) -> Decimal:
        """Get subtotal before discount."""
        return self.unit_price * self.quantity
    
    @classmethod
    def from_cart_item(cls, cart_item, order_id: int) -> "OrderItem":
        """Create OrderItem from CartItem."""
        product = cart_item.product
        return cls(
            order_id=order_id,
            product_id=product.id,
            seller_id=product.seller_id,
            product_name=product.name,
            product_sku=product.sku,
            product_image=product.main_image,
            unit_price=product.current_price,
            quantity=cart_item.quantity,
            discount_amount=product.discount_amount if product.has_discount else Decimal(0),
            total_price=product.current_price * cart_item.quantity,
        )
