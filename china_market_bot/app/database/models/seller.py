"""
🏪 Seller Model Module

Seller profile database model.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.constants import ModerationStatus

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class Seller(Base, IDMixin, TimestampMixin):
    """
    Seller model representing marketplace sellers.
    
    Links to User model and contains seller-specific information.
    """
    
    __tablename__ = "sellers"
    
    # User relationship
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
        comment="Reference to user",
    )
    
    # Business Info
    company_name: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        comment="Company or store name",
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Seller description",
    )
    logo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Logo image URL",
    )
    
    # Contact Info
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Business phone number",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Business email",
    )
    address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Business address",
    )
    
    # Legal Info
    inn: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="INN (tax ID)",
    )
    license_number: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Business license number",
    )
    
    # Moderation
    moderation_status: Mapped[ModerationStatus] = mapped_column(
        Enum(ModerationStatus, name="seller_moderation_status"),
        default=ModerationStatus.PENDING,
        nullable=False,
        comment="Moderation status",
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Reason for rejection",
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When seller was approved",
    )
    approved_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Admin ID who approved",
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Is seller active",
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is seller verified",
    )
    
    # Statistics
    total_sales: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Total number of sales",
    )
    total_revenue: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        comment="Total revenue in UZS",
    )
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
    
    # Commission
    commission_rate: Mapped[float] = mapped_column(
        Float,
        default=5.0,
        nullable=False,
        comment="Commission rate in percent",
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="seller_profile",
        lazy="selectin",
    )
    
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="seller",
        lazy="selectin",
        order_by="desc(Product.created_at)",
    )
    
    # Properties
    @property
    def is_approved(self) -> bool:
        """Check if seller is approved."""
        return self.moderation_status == ModerationStatus.APPROVED
    
    @property
    def product_count(self) -> int:
        """Get active product count."""
        return len([p for p in self.products if p.is_active])
    
    def approve(self, admin_id: int) -> None:
        """Approve seller."""
        self.moderation_status = ModerationStatus.APPROVED
        self.approved_at = datetime.utcnow()
        self.approved_by = admin_id
        self.rejection_reason = None
    
    def reject(self, reason: str) -> None:
        """Reject seller application."""
        self.moderation_status = ModerationStatus.REJECTED
        self.rejection_reason = reason
    
    def suspend(self, reason: str) -> None:
        """Suspend seller."""
        self.moderation_status = ModerationStatus.SUSPENDED
        self.rejection_reason = reason
        self.is_active = False
