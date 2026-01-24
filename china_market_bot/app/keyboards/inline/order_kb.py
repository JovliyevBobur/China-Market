"""
📋 Order Keyboards Module

Inline keyboards for order management.
"""

from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks import (
    OrderCallback,
    DeliveryCallback,
    PaymentCallback,
    BackCallback,
    ConfirmCallback,
)
from app.config.constants import DeliveryType, PaymentMethod, OrderStatus
from app.database.models import Order


def get_delivery_keyboard() -> InlineKeyboardMarkup:
    """
    Get delivery type selection keyboard.
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="🏪 O'zi olib ketadi (Bepul)",
        callback_data=DeliveryCallback(type=DeliveryType.PICKUP.value).pack(),
    )
    builder.button(
        text="🚚 Oddiy yetkazib berish",
        callback_data=DeliveryCallback(type=DeliveryType.STANDARD.value).pack(),
    )
    builder.button(
        text="⚡ Tez yetkazib berish",
        callback_data=DeliveryCallback(type=DeliveryType.EXPRESS.value).pack(),
    )
    
    builder.adjust(1)
    
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=BackCallback(to="cart").pack(),
    )
    
    return builder.as_markup()


def get_payment_keyboard(
    stars_enabled: bool = True,
) -> InlineKeyboardMarkup:
    """
    Get payment method selection keyboard.
    
    Args:
        stars_enabled: Enable Telegram Stars
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    if stars_enabled:
        builder.button(
            text="⭐ Telegram Stars",
            callback_data=PaymentCallback(method=PaymentMethod.TELEGRAM_STARS.value).pack(),
        )
    
    builder.button(
        text="💳 Click",
        callback_data=PaymentCallback(method=PaymentMethod.CLICK.value).pack(),
    )
    builder.button(
        text="💳 Payme",
        callback_data=PaymentCallback(method=PaymentMethod.PAYME.value).pack(),
    )
    builder.button(
        text="💵 Naqd pul",
        callback_data=PaymentCallback(method=PaymentMethod.CASH.value).pack(),
    )
    
    builder.adjust(1)
    
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=BackCallback(to="delivery").pack(),
    )
    
    return builder.as_markup()


def get_order_confirm_keyboard(order_id: int = 0) -> InlineKeyboardMarkup:
    """
    Get order confirmation keyboard.
    
    Args:
        order_id: Order ID (0 for new order)
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✅ Buyurtmani tasdiqlash",
        callback_data=ConfirmCallback(
            action="yes",
            context="order",
            data=order_id,
        ).pack(),
    )
    builder.button(
        text="❌ Bekor qilish",
        callback_data=ConfirmCallback(
            action="no",
            context="order",
            data=order_id,
        ).pack(),
    )
    
    builder.adjust(1)
    
    return builder.as_markup()


def get_order_view_keyboard(order: Order) -> InlineKeyboardMarkup:
    """
    Get order view keyboard.
    
    Args:
        order: Order model
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Status-specific actions
    if order.can_cancel:
        builder.button(
            text="❌ Bekor qilish",
            callback_data=OrderCallback(
                action="cancel",
                order_id=order.id,
            ).pack(),
        )
    
    if order.status == OrderStatus.SHIPPED:
        builder.button(
            text="📍 Kuzatish",
            callback_data=OrderCallback(
                action="track",
                order_id=order.id,
            ).pack(),
        )
    
    if order.status == OrderStatus.COMPLETED:
        builder.button(
            text="⭐ Baholash",
            callback_data=OrderCallback(
                action="rate",
                order_id=order.id,
            ).pack(),
        )
        builder.button(
            text="🔄 Qayta buyurtma",
            callback_data=OrderCallback(
                action="reorder",
                order_id=order.id,
            ).pack(),
        )
    
    builder.adjust(2)
    
    # Support
    builder.row()
    builder.button(
        text="💬 Yordam",
        callback_data=OrderCallback(
            action="support",
            order_id=order.id,
        ).pack(),
    )
    
    # Back
    builder.row()
    builder.button(
        text="⬅️ Buyurtmalar ro'yxati",
        callback_data=BackCallback(to="orders").pack(),
    )
    
    return builder.as_markup()


def get_orders_list_keyboard(
    orders: List[Order],
    page: int = 1,
    total_pages: int = 1,
) -> InlineKeyboardMarkup:
    """
    Get orders list keyboard.
    
    Args:
        orders: List of orders
        page: Current page
        total_pages: Total pages
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Status emojis
    status_emoji = {
        OrderStatus.PENDING: "⏳",
        OrderStatus.CONFIRMED: "✅",
        OrderStatus.PROCESSING: "📦",
        OrderStatus.SHIPPED: "🚚",
        OrderStatus.DELIVERED: "📬",
        OrderStatus.COMPLETED: "🎉",
        OrderStatus.CANCELLED: "❌",
        OrderStatus.REFUNDED: "💸",
    }
    
    for order in orders:
        emoji = status_emoji.get(order.status, "📋")
        total = f"{order.total_amount:,.0f}".replace(",", " ")
        
        builder.button(
            text=f"{emoji} #{order.order_number} - {total} so'm",
            callback_data=OrderCallback(
                action="view",
                order_id=order.id,
            ).pack(),
        )
    
    builder.adjust(1)
    
    # Pagination
    if total_pages > 1:
        builder.row()
        
        if page > 1:
            builder.button(
                text="◀️",
                callback_data=OrderCallback(
                    action=f"page_{page - 1}",
                    order_id=0,
                ).pack(),
            )
        
        builder.button(text=f"{page}/{total_pages}", callback_data="noop")
        
        if page < total_pages:
            builder.button(
                text="▶️",
                callback_data=OrderCallback(
                    action=f"page_{page + 1}",
                    order_id=0,
                ).pack(),
            )
    
    # Navigation
    builder.row()
    builder.button(
        text="🏠 Asosiy menyu",
        callback_data=BackCallback(to="main").pack(),
    )
    
    return builder.as_markup()


def get_order_cancel_confirm_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """
    Get order cancel confirmation keyboard.
    
    Args:
        order_id: Order ID
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✅ Ha, bekor qilish",
        callback_data=ConfirmCallback(
            action="yes",
            context="cancel_order",
            data=order_id,
        ).pack(),
    )
    builder.button(
        text="❌ Yo'q, qaytish",
        callback_data=OrderCallback(
            action="view",
            order_id=order_id,
        ).pack(),
    )
    
    builder.adjust(1)
    
    return builder.as_markup()
