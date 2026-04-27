"""
💳 Payment Model Module

Payment database model for tracking transactions.
"""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.constants import PaymentMethod, PaymentStatus

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .order import Order


class Payment(Base, IDMixin, TimestampMixin):
    """
    Payment model for tracking transactions.
    
    Stores payment details, status, and provider-specific data.
    """
    
    __tablename__ = "payments"
    
    # Order relationship
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to order",
    )
    
    # Payment identifiers
    transaction_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Internal transaction ID",
    )
    external_id: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        index=True,
        comment="External provider transaction ID",
    )
    
    # Payment details
    method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method_type"),
        nullable=False,
        comment="Payment method",
    )
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status_type"),
        default=PaymentStatus.PENDING,
        nullable=False,
        index=True,
        comment="Payment status",
    )
    
    # Amount
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Payment amount",
    )
    currency: Mapped[str] = mapped_column(
        String(10),
        default="UZS",
        nullable=False,
        comment="Currency code",
    )
    
    # For Telegram Stars
    stars_amount: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Amount in Telegram Stars",
    )
    
    # Provider data
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Payment provider name",
    )
    provider_data: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Provider-specific data as JSON",
    )
    
    # URLs
    payment_url: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
        comment="Payment URL for redirect",
    )
    
    # Timestamps
    initiated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        comment="When payment was initiated",
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When payment was completed",
    )
    failed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When payment failed",
    )
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When payment was cancelled",
    )
    refunded_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When payment was refunded",
    )
    
    # Error info
    error_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Error code if failed",
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Error message if failed",
    )
    
    # Refund info
    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        default=Decimal(0),
        nullable=False,
        comment="Refunded amount",
    )
    refund_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Reason for refund",
    )
    
    # IP and metadata
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Client IP address",
    )
    user_agent: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Client user agent",
    )
    
    # Relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payments",
        lazy="selectin",
    )
    
    # Properties
    @property
    def is_successful(self) -> bool:
        """Check if payment was successful."""
        return self.status == PaymentStatus.COMPLETED
    
    @property
    def is_pending(self) -> bool:
        """Check if payment is pending."""
        return self.status in (PaymentStatus.PENDING, PaymentStatus.PROCESSING)
    
    @property
    def is_refundable(self) -> bool:
        """Check if payment can be refunded."""
        return (
            self.status == PaymentStatus.COMPLETED
            and self.refund_amount < self.amount
        )
    
    @property
    def remaining_refundable(self) -> Decimal:
        """Get remaining refundable amount."""
        return self.amount - self.refund_amount
    
    def mark_completed(self, external_id: Optional[str] = None) -> None:
        """Mark payment as completed."""
        self.status = PaymentStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if external_id:
            self.external_id = external_id
    
    def mark_failed(self, error_code: str, error_message: str) -> None:
        """Mark payment as failed."""
        self.status = PaymentStatus.FAILED
        self.failed_at = datetime.utcnow()
        self.error_code = error_code
        self.error_message = error_message
    
    def mark_cancelled(self) -> None:
        """Mark payment as cancelled."""
        self.status = PaymentStatus.CANCELLED
        self.cancelled_at = datetime.utcnow()
    
    def process_refund(self, amount: Decimal, reason: str) -> bool:
        """Process refund."""
        if amount > self.remaining_refundable:
            return False
        
        self.refund_amount += amount
        self.refund_reason = reason
        self.refunded_at = datetime.utcnow()
        
        if self.refund_amount >= self.amount:
            self.status = PaymentStatus.REFUNDED
        
        return True
