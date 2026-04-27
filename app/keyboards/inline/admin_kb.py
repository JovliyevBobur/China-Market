"""
👑 Admin Keyboards Module

Inline keyboards for admin panel.
"""

from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks import (
    AdminCallback,
    UserManageCallback,
    ModerationCallback,
    BroadcastCallback,
    CategoryManageCallback,
    BackCallback,
    ConfirmCallback,
)
from app.database.models import User, Product, Category


def get_admin_dashboard_keyboard() -> InlineKeyboardMarkup:
    """
    Get admin dashboard keyboard.
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Stats
    builder.button(
        text="📊 Statistika",
        callback_data=AdminCallback(action="stats").pack(),
    )
    builder.button(
        text="👥 Foydalanuvchilar",
        callback_data=AdminCallback(action="users").pack(),
    )
    
    # Moderation
    builder.button(
        text="🏪 Sotuvchilar",
        callback_data=AdminCallback(action="sellers").pack(),
    )
    builder.button(
        text="📦 Moderatsiya",
        callback_data=AdminCallback(action="moderation").pack(),
    )
    
    # Management
    builder.button(
        text="📁 Kategoriyalar",
        callback_data=AdminCallback(action="categories").pack(),
    )
    builder.button(
        text="📋 Buyurtmalar",
        callback_data=AdminCallback(action="orders").pack(),
    )
    
    # Communication
    builder.button(
        text="📢 Xabar yuborish",
        callback_data=AdminCallback(action="broadcast").pack(),
    )
    builder.button(
        text="⚙️ Sozlamalar",
        callback_data=AdminCallback(action="settings").pack(),
    )
    
    builder.adjust(2)
    
    return builder.as_markup()


def get_user_manage_keyboard(user: User) -> InlineKeyboardMarkup:
    """
    Get user management keyboard.
    
    Args:
        user: User model
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Ban/Unban
    if user.is_banned:
        builder.button(
            text="✅ Blokdan chiqarish",
            callback_data=UserManageCallback(
                action="unban",
                user_id=user.id,
            ).pack(),
        )
    else:
        builder.button(
            text="🚫 Bloklash",
            callback_data=UserManageCallback(
                action="ban",
                user_id=user.id,
            ).pack(),
        )
    
    # Role
    builder.button(
        text="👑 Rol o'zgartirish",
        callback_data=UserManageCallback(
            action="role",
            user_id=user.id,
        ).pack(),
    )
    
    # Message
    builder.button(
        text="💬 Xabar yuborish",
        callback_data=UserManageCallback(
            action="message",
            user_id=user.id,
        ).pack(),
    )
    
    builder.adjust(2)
    
    # Back
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=AdminCallback(action="users").pack(),
    )
    
    return builder.as_markup()


def get_moderation_keyboard(
    item_type: str,
    item_id: int,
) -> InlineKeyboardMarkup:
    """
    Get moderation keyboard.
    
    Args:
        item_type: Type of item (product/seller)
        item_id: Item ID
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Approve
    builder.button(
        text="✅ Tasdiqlash",
        callback_data=ModerationCallback(
            action="approve",
            type=item_type,
            id=item_id,
        ).pack(),
    )
    
    # Reject
    builder.button(
        text="❌ Rad etish",
        callback_data=ModerationCallback(
            action="reject",
            type=item_type,
            id=item_id,
        ).pack(),
    )
    
    builder.adjust(2)
    
    # Skip
    builder.row()
    builder.button(
        text="⏭️ Keyingi",
        callback_data=ModerationCallback(
            action="skip",
            type=item_type,
            id=item_id,
        ).pack(),
    )
    
    # Back
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=AdminCallback(action="moderation").pack(),
    )
    
    return builder.as_markup()


def get_broadcast_keyboard() -> InlineKeyboardMarkup:
    """
    Get broadcast settings keyboard.
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Audience
    builder.button(
        text="👥 Barcha foydalanuvchilar",
        callback_data=BroadcastCallback(action="audience", data="all").pack(),
    )
    builder.button(
        text="🏪 Faqat sotuvchilar",
        callback_data=BroadcastCallback(action="audience", data="sellers").pack(),
    )
    builder.button(
        text="🛒 Faol xaridorlar",
        callback_data=BroadcastCallback(action="audience", data="active").pack(),
    )
    
    builder.adjust(1)
    
    # Back
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=AdminCallback(action="dashboard").pack(),
    )
    
    return builder.as_markup()


def get_categories_manage_keyboard(
    categories: List[Category],
) -> InlineKeyboardMarkup:
    """
    Get categories management keyboard.
    
    Args:
        categories: List of categories
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    for category in categories:
        icon = category.icon or "📁"
        builder.button(
            text=f"{icon} {category.name}",
            callback_data=CategoryManageCallback(
                action="view",
                category_id=category.id,
            ).pack(),
        )
    
    builder.adjust(2)
    
    # Add new
    builder.row()
    builder.button(
        text="➕ Yangi kategoriya",
        callback_data=CategoryManageCallback(
            action="add",
            category_id=0,
        ).pack(),
    )
    
    # Back
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=AdminCallback(action="dashboard").pack(),
    )
    
    return builder.as_markup()


def get_category_edit_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """
    Get category edit keyboard.
    
    Args:
        category_id: Category ID
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✏️ Nomni o'zgartirish",
        callback_data=CategoryManageCallback(
            action="edit_name",
            category_id=category_id,
        ).pack(),
    )
    builder.button(
        text="🎨 Ikonkani o'zgartirish",
        callback_data=CategoryManageCallback(
            action="edit_icon",
            category_id=category_id,
        ).pack(),
    )
    builder.button(
        text="🗑️ O'chirish",
        callback_data=CategoryManageCallback(
            action="delete",
            category_id=category_id,
        ).pack(),
    )
    
    builder.adjust(2)
    
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=AdminCallback(action="categories").pack(),
    )
    
    return builder.as_markup()


def get_confirm_broadcast_keyboard(count: int) -> InlineKeyboardMarkup:
    """
    Get broadcast confirmation keyboard.
    
    Args:
        count: Number of recipients
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=f"✅ Yuborish ({count} ta foydalanuvchi)",
        callback_data=ConfirmCallback(
            action="yes",
            context="broadcast",
        ).pack(),
    )
    builder.button(
        text="❌ Bekor qilish",
        callback_data=ConfirmCallback(
            action="no",
            context="broadcast",
        ).pack(),
    )
    
    builder.adjust(1)
    
    return builder.as_markup()
