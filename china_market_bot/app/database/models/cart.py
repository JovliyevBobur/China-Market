"""
🛒 Cart Model Module

Cart and CartItem database models.
"""

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class CartItem(Base, IDMixin, TimestampMixin):
    """
    Cart item model representing items in user's cart.
    
    Each user can have multiple cart items.
    """
    
    __tablename__ = "cart_items"
    
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_cart_user_product"),
    )
    
    # Relationships
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to user",
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to product",
    )
    
    # Quantity
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="Quantity in cart",
    )
    
    # Price snapshot (at the time of adding to cart)
    price_snapshot: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Price when added to cart",
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="cart_items",
        lazy="selectin",
    )
    
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="cart_items",
        lazy="selectin",
    )
    
    # Properties
    @property
    def total_price(self) -> Decimal:
        """Get total price for this cart item."""
        return self.price_snapshot * self.quantity
    
    @property
    def current_price(self) -> Decimal:
        """Get current product price."""
        return self.product.current_price
    
    @property
    def price_changed(self) -> bool:
        """Check if price has changed since adding to cart."""
        return self.price_snapshot != self.current_price
    
    @property
    def is_available(self) -> bool:
        """Check if product is available."""
        return (
            self.product.is_active
            and self.product.is_approved
            and self.product.available_quantity >= self.quantity
        )
    
    def update_quantity(self, qty: int) -> bool:
        """Update quantity if valid."""
        if qty <= 0:
            return False
        if qty > self.product.available_quantity:
            return False
        if self.product.max_order_quantity and qty > self.product.max_order_quantity:
            return False
        self.quantity = qty
        return True
    
    def update_price_snapshot(self) -> None:
        """Update price snapshot to current product price."""
        self.price_snapshot = self.product.current_price


class Cart:
    """
    Cart utility class for cart operations.
    
    This is not a database model, but a helper class.
    """
    
    def __init__(self, items: list[CartItem]):
        self.items = items
    
    @property
    def total(self) -> Decimal:
        """Get total cart value."""
        return sum(item.total_price for item in self.items)
    
    @property
    def item_count(self) -> int:
        """Get number of unique items."""
        return len(self.items)
    
    @property
    def total_quantity(self) -> int:
        """Get total quantity of all items."""
        return sum(item.quantity for item in self.items)
    
    @property
    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self.items) == 0
    
    @property
    def all_available(self) -> bool:
        """Check if all items are available."""
        return all(item.is_available for item in self.items)
    
    @property
    def unavailable_items(self) -> list[CartItem]:
        """Get list of unavailable items."""
        return [item for item in self.items if not item.is_available]
