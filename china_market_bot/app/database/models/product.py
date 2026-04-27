"""
📦 Product Model Module

Product database model with all related fields.
"""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.constants import ModerationStatus

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .cart import CartItem
    from .category import Category
    from .order import OrderItem
    from .review import Review
    from .seller import Seller


class Product(Base, IDMixin, TimestampMixin):
    """
    Product model representing marketplace items.
    
    Contains all product information including pricing,
    inventory, media, and moderation status.
    """
    
    __tablename__ = "products"
    
    # Relationships
    seller_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to seller",
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Reference to category",
    )
    
    # Basic Info
    name: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        index=True,
        comment="Product name",
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Product description",
    )
    short_description: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Short description for previews",
    )
    
    # SKU
    sku: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
        comment="Stock Keeping Unit",
    )
    
    # Pricing
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Price in UZS",
    )
    discount_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=True,
        comment="Discounted price in UZS",
    )
    discount_percent: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Discount percentage",
    )
    discount_ends_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When discount ends",
    )
    
    # Stars pricing
    stars_price: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Price in Telegram Stars",
    )
    
    # Inventory
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Available quantity",
    )
    reserved_quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Reserved in orders",
    )
    min_order_quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="Minimum order quantity",
    )
    max_order_quantity: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Maximum order quantity",
    )
    
    # Statistics
    sold_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Total units sold",
    )
    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Total views",
    )
    
    # Media - PostgreSQL array type
    images: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        nullable=True,
        comment="Array of image URLs",
    )
    video_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Video URL",
    )
    external_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="External website URL for direct redirect",
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Is product active",
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is product featured",
    )
    
    # Moderation
    moderation_status: Mapped[ModerationStatus] = mapped_column(
        Enum(ModerationStatus, name="product_moderation_status"),
        default=ModerationStatus.PENDING,
        nullable=False,
        comment="Moderation status",
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Reason for rejection",
    )
    moderated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When product was moderated",
    )
    moderated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Moderator user ID",
    )
    
    # SEO
    slug: Mapped[str] = mapped_column(
        String(350),
        unique=True,
        nullable=False,
        index=True,
        comment="URL-friendly slug",
    )
    meta_title: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="SEO meta title",
    )
    meta_description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="SEO meta description",
    )
    
    # Rating
    rating: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        comment="Average rating",
    )
    review_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of reviews",
    )
    
    # Product specs (JSON-like string, could be JSONB)
    specifications: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Product specifications as JSON",
    )
    
    # Weight and dimensions
    weight: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Weight in kg",
    )
    
    # Relationships
    seller: Mapped["Seller"] = relationship(
        "Seller",
        back_populates="products",
        lazy="selectin",
    )
    
    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="products",
        lazy="selectin",
    )
    
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="product",
        lazy="selectin",
        order_by="desc(Review.created_at)",
    )
    
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="product",
        lazy="selectin",
    )
    
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product",
        lazy="selectin",
    )
    
    # Properties
    @property
    def current_price(self) -> Decimal:
        """Get current price (discounted if applicable)."""
        if self.has_discount:
            return self.discount_price
        return self.price
    
    @property
    def has_discount(self) -> bool:
        """Check if product has active discount."""
        if not self.discount_price:
            return False
        if self.discount_ends_at and self.discount_ends_at < datetime.utcnow():
            return False
        return self.discount_price < self.price
    
    @property
    def discount_amount(self) -> Decimal:
        """Get discount amount."""
        if self.has_discount:
            return self.price - self.discount_price
        return Decimal(0)
    
    @property
    def available_quantity(self) -> int:
        """Get available quantity (total - reserved)."""
        return max(0, self.quantity - self.reserved_quantity)
    
    @property
    def is_in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.available_quantity > 0
    
    @property
    def is_approved(self) -> bool:
        """Check if product is approved."""
        return self.moderation_status == ModerationStatus.APPROVED
    
    @property
    def main_image(self) -> Optional[str]:
        """Get main product image."""
        if self.images and len(self.images) > 0:
            return self.images[0]
        return None
    
    def increment_view(self) -> None:
        """Increment view count."""
        self.view_count += 1
    
    def reserve_quantity(self, qty: int) -> bool:
        """Reserve quantity for an order."""
        if qty <= self.available_quantity:
            self.reserved_quantity += qty
            return True
        return False
    
    def release_quantity(self, qty: int) -> None:
        """Release reserved quantity."""
        self.reserved_quantity = max(0, self.reserved_quantity - qty)
    
    def confirm_sale(self, qty: int) -> None:
        """Confirm sale - reduce stock and update stats."""
        self.quantity -= qty
        self.reserved_quantity -= qty
        self.sold_count += qty
    
    def update_rating(self, new_rating: float, is_new_review: bool = True) -> None:
        """Update product rating."""
        if is_new_review:
            total = self.rating * self.review_count + new_rating
            self.review_count += 1
            self.rating = total / self.review_count
        else:
            # Recalculate from reviews if needed
            pass
