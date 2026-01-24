"""
🛒 Cart Keyboards Module

Inline keyboards for cart management.
"""

from decimal import Decimal
from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks import CartCallback, CartItemCallback, CheckoutCallback, BackCallback
from app.database.models import CartItem


def get_cart_keyboard(
    items: List[CartItem],
    total: Decimal,
) -> InlineKeyboardMarkup:
    """
    Get cart view keyboard.
    
    Args:
        items: List of cart items
        total: Cart total
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Cart items
    for item in items:
        price = f"{item.total_price:,.0f}".replace(",", " ")
        builder.button(
            text=f"📦 {item.product.name[:20]}... x{item.quantity}",
            callback_data=CartItemCallback(
                action="view",
                item_id=item.id,
            ).pack(),
        )
    
    builder.adjust(1)
    
    # Cart actions
    builder.row()
    builder.button(
        text="🗑️ Savatni tozalash",
        callback_data=CartCallback(action="clear").pack(),
    )
    builder.button(
        text="🔄 Yangilash",
        callback_data=CartCallback(action="refresh").pack(),
    )
    
    # Checkout
    total_text = f"{total:,.0f}".replace(",", " ")
    builder.row()
    builder.button(
        text=f"💳 To'lash ({total_text} so'm)",
        callback_data=CheckoutCallback(step="start").pack(),
    )
    
    # Navigation
    builder.row()
    builder.button(
        text="🛍️ Xarid qilishda davom etish",
        callback_data=BackCallback(to="catalog").pack(),
    )
    
    return builder.as_markup()


def get_cart_item_keyboard(
    item: CartItem,
    max_quantity: int,
) -> InlineKeyboardMarkup:
    """
    Get cart item management keyboard.
    
    Args:
        item: Cart item
        max_quantity: Maximum allowed quantity
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Quantity selector
    builder.row()
    builder.button(
        text="➖",
        callback_data=CartItemCallback(
            action="dec",
            item_id=item.id,
        ).pack(),
    )
    builder.button(
        text=f"📦 {item.quantity}",
        callback_data="noop",
    )
    builder.button(
        text="➕",
        callback_data=CartItemCallback(
            action="inc",
            item_id=item.id,
        ).pack(),
    )
    
    # Quick quantity options
    builder.row()
    for qty in [1, 5, 10]:
        if qty <= max_quantity:
            builder.button(
                text=f"{qty} dona",
                callback_data=CartItemCallback(
                    action=f"set_{qty}",
                    item_id=item.id,
                ).pack(),
            )
    
    # Remove
    builder.row()
    builder.button(
        text="🗑️ O'chirish",
        callback_data=CartItemCallback(
            action="remove",
            item_id=item.id,
        ).pack(),
    )
    
    # Back to cart
    builder.row()
    builder.button(
        text="⬅️ Savatga qaytish",
        callback_data=CartCallback(action="view").pack(),
    )
    
    return builder.as_markup()


def get_empty_cart_keyboard() -> InlineKeyboardMarkup:
    """
    Get empty cart keyboard.
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="🛍️ Katalogga o'tish",
        callback_data=BackCallback(to="catalog").pack(),
    )
    
    return builder.as_markup()


def get_checkout_keyboard() -> InlineKeyboardMarkup:
    """
    Get checkout start keyboard.
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✅ Buyurtma berish",
        callback_data=CheckoutCallback(step="confirm").pack(),
    )
    builder.button(
        text="⬅️ Savatga qaytish",
        callback_data=CartCallback(action="view").pack(),
    )
    
    builder.adjust(1)
    
    return builder.as_markup()


def get_cart_validation_keyboard(
    has_unavailable: bool = False,
    has_price_changed: bool = False,
) -> InlineKeyboardMarkup:
    """
    Get cart validation keyboard.
    
    Args:
        has_unavailable: Has unavailable items
        has_price_changed: Has items with changed prices
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    if has_unavailable:
        builder.button(
            text="🗑️ Mavjud bo'lmaganlarni o'chirish",
            callback_data=CartCallback(action="remove_unavailable").pack(),
        )
    
    if has_price_changed:
        builder.button(
            text="🔄 Narxlarni yangilash",
            callback_data=CartCallback(action="update_prices").pack(),
        )
    
    builder.adjust(1)
    
    builder.row()
    builder.button(
        text="⬅️ Savatga qaytish",
        callback_data=CartCallback(action="view").pack(),
    )
    
    return builder.as_markup()
