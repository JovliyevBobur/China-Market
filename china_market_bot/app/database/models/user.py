"""
👤 User Model Module

User database model with all related fields and relationships.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.constants import Language, UserRole

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .cart import CartItem
    from .order import Order
    from .review import Review
    from .seller import Seller


class User(Base, IDMixin, TimestampMixin):
    """
    User model representing Telegram users.
    
    Stores user information, preferences, and relationships
    to orders, cart items, reviews, and seller profile.
    """
    
    __tablename__ = "users"
    
    # Telegram Info
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
        comment="Telegram user ID",
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Telegram username without @",
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="User's first name",
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="User's last name",
    )
    
    # Contact Info
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        index=True,
        comment="Phone number with country code",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Email address",
    )
    
    # Preferences
    language: Mapped[str] = mapped_column(
        String(5),
        default=Language.UZ.value,
        nullable=False,
        comment="Preferred language code",
    )
    
    # Role & Permissions
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        default=UserRole.USER,
        nullable=False,
        comment="User role",
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Is user active",
    )
    is_banned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is user banned",
    )
    ban_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Reason for ban",
    )
    banned_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When user was banned",
    )
    
    # Verification
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is phone verified",
    )
    
    # Activity
    last_activity: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        comment="Last activity timestamp",
    )
    
    # Relationships
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
        lazy="selectin",
        order_by="desc(Order.created_at)",
    )
    
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
        lazy="selectin",
    )
    
    seller_profile: Mapped[Optional["Seller"]] = relationship(
        "Seller",
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )
    
    # Properties
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) or "Foydalanuvchi"
    
    @property
    def mention(self) -> str:
        """Get user mention for Telegram."""
        return f"<a href='tg://user?id={self.telegram_id}'>{self.full_name}</a>"
    
    @property
    def is_seller(self) -> bool:
        """Check if user is a seller."""
        return self.role in (UserRole.SELLER, UserRole.ADMIN, UserRole.SUPERADMIN)
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role in (UserRole.ADMIN, UserRole.SUPERADMIN, UserRole.MODERATOR)
    
    def ban(self, reason: str) -> None:
        """Ban user with reason."""
        self.is_banned = True
        self.ban_reason = reason
        self.banned_at = datetime.utcnow()
    
    def unban(self) -> None:
        """Unban user."""
        self.is_banned = False
        self.ban_reason = None
        self.banned_at = None
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
