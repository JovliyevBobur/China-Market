"""
⭐ Review Model Module

Review database model for product reviews and ratings.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class Review(Base, IDMixin, TimestampMixin):
    """
    Review model for product reviews and ratings.
    
    Users can leave one review per product.
    """
    
    __tablename__ = "reviews"
    
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_review_user_product"),
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
    order_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="SET NULL"),
        nullable=True,
        comment="Reference to order (verified purchase)",
    )
    
    # Rating
    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Rating 1-5 stars",
    )
    
    # Review content
    title: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="Review title",
    )
    content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Review content",
    )
    
    # Media
    images: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        nullable=True,
        comment="Review images",
    )
    
    # Pros and cons
    pros: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Positive aspects",
    )
    cons: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Negative aspects",
    )
    
    # Status
    is_verified_purchase: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is this a verified purchase review",
    )
    is_approved: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Is review approved",
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is review featured",
    )
    
    # Helpfulness
    helpful_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of users who found this helpful",
    )
    not_helpful_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of users who found this not helpful",
    )
    
    # Seller response
    seller_response: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Seller response to review",
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews",
        lazy="selectin",
    )
    
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews",
        lazy="selectin",
    )
    
    # Properties
    @property
    def rating_emoji(self) -> str:
        """Get rating as star emojis."""
        return "⭐" * self.rating
    
    @property
    def helpfulness_score(self) -> float:
        """Calculate helpfulness score."""
        total = self.helpful_count + self.not_helpful_count
        if total == 0:
            return 0.0
        return self.helpful_count / total
    
    def mark_helpful(self) -> None:
        """Mark review as helpful."""
        self.helpful_count += 1
    
    def mark_not_helpful(self) -> None:
        """Mark review as not helpful."""
        self.not_helpful_count += 1
