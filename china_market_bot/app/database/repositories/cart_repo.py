"""
🛒 Cart Repository Module

Repository for cart-related database operations.
"""

from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import delete, func, select
from sqlalchemy.orm import selectinload

from app.database.models import Cart, CartItem, Product

from .base_repo import BaseRepository


class CartRepository(BaseRepository[CartItem]):
    """
    Cart repository with specialized queries.
    """
    
    model = CartItem
    
    async def get_user_cart(self, user_id: int) -> Cart:
        """
        Get user's cart with all items.
        
        Args:
            user_id: User ID
        
        Returns:
            Cart object with items
        """
        result = await self.session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
            .order_by(CartItem.created_at.desc())
        )
        items = list(result.scalars().all())
        return Cart(items=items)
    
    async def get_cart_items(self, user_id: int) -> Sequence[CartItem]:
        """
        Get all cart items for user.
        
        Args:
            user_id: User ID
        
        Returns:
            Sequence of cart items
        """
        result = await self.session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
            .order_by(CartItem.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_cart_item(
        self,
        user_id: int,
        product_id: int,
    ) -> Optional[CartItem]:
        """
        Get specific cart item.
        
        Args:
            user_id: User ID
            product_id: Product ID
        
        Returns:
            CartItem or None
        """
        result = await self.session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
        )
        return result.scalar_one_or_none()
    
    async def add_to_cart(
        self,
        user_id: int,
        product_id: int,
        quantity: int = 1,
    ) -> CartItem:
        """
        Add product to cart or update quantity.
        
        Args:
            user_id: User ID
            product_id: Product ID
            quantity: Quantity to add
        
        Returns:
            CartItem (new or updated)
        """
        # Check if item already in cart
        cart_item = await self.get_cart_item(user_id, product_id)
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
            await self.session.flush()
            await self.session.refresh(cart_item)
            return cart_item
        
        # Get product for price
        product = await self.session.get(Product, product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        # Create new cart item
        cart_item = await self.create(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            price_snapshot=product.current_price,
        )
        
        return cart_item
    
    async def update_quantity(
        self,
        user_id: int,
        product_id: int,
        quantity: int,
    ) -> Optional[CartItem]:
        """
        Update cart item quantity.
        
        Args:
            user_id: User ID
            product_id: Product ID
            quantity: New quantity
        
        Returns:
            Updated CartItem or None
        """
        cart_item = await self.get_cart_item(user_id, product_id)
        
        if not cart_item:
            return None
        
        if quantity <= 0:
            await self.remove_from_cart(user_id, product_id)
            return None
        
        cart_item.quantity = quantity
        await self.session.flush()
        await self.session.refresh(cart_item)
        
        return cart_item
    
    async def remove_from_cart(
        self,
        user_id: int,
        product_id: int,
    ) -> bool:
        """
        Remove product from cart.
        
        Args:
            user_id: User ID
            product_id: Product ID
        
        Returns:
            True if removed, False if not found
        """
        result = await self.session.execute(
            delete(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
        )
        await self.session.flush()
        return result.rowcount > 0
    
    async def clear_cart(self, user_id: int) -> int:
        """
        Clear all items from user's cart.
        
        Args:
            user_id: User ID
        
        Returns:
            Number of items removed
        """
        result = await self.session.execute(
            delete(CartItem).where(CartItem.user_id == user_id)
        )
        await self.session.flush()
        return result.rowcount
    
    async def get_cart_total(self, user_id: int) -> Decimal:
        """
        Get total value of user's cart.
        
        Args:
            user_id: User ID
        
        Returns:
            Total cart value
        """
        result = await self.session.execute(
            select(
                func.sum(CartItem.price_snapshot * CartItem.quantity)
            ).where(CartItem.user_id == user_id)
        )
        total = result.scalar_one()
        return total or Decimal(0)
    
    async def get_cart_count(self, user_id: int) -> int:
        """
        Get number of items in user's cart.
        
        Args:
            user_id: User ID
        
        Returns:
            Number of unique items
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(CartItem)
            .where(CartItem.user_id == user_id)
        )
        return result.scalar_one()
    
    async def get_cart_quantity(self, user_id: int) -> int:
        """
        Get total quantity of all items in cart.
        
        Args:
            user_id: User ID
        
        Returns:
            Total quantity
        """
        result = await self.session.execute(
            select(func.sum(CartItem.quantity))
            .where(CartItem.user_id == user_id)
        )
        total = result.scalar_one()
        return total or 0
    
    async def update_prices(self, user_id: int) -> int:
        """
        Update all cart item price snapshots to current prices.
        
        Args:
            user_id: User ID
        
        Returns:
            Number of items updated
        """
        cart_items = await self.get_cart_items(user_id)
        updated = 0
        
        for item in cart_items:
            if item.price_changed:
                item.update_price_snapshot()
                updated += 1
        
        if updated > 0:
            await self.session.flush()
        
        return updated
    
    async def validate_cart(self, user_id: int) -> dict:
        """
        Validate cart items (availability, stock, etc.).
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with validation results
        """
        cart = await self.get_user_cart(user_id)
        
        unavailable = []
        out_of_stock = []
        price_changed = []
        
        for item in cart.items:
            if not item.product.is_active or not item.product.is_approved:
                unavailable.append(item)
            elif item.product.available_quantity < item.quantity:
                out_of_stock.append(item)
            elif item.price_changed:
                price_changed.append(item)
        
        return {
            "valid": len(unavailable) == 0 and len(out_of_stock) == 0,
            "unavailable": unavailable,
            "out_of_stock": out_of_stock,
            "price_changed": price_changed,
            "total": cart.total,
            "item_count": cart.item_count,
        }
