"""
🏠 Main Menu Keyboards Module

Reply keyboards for main menu.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get main menu keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = MENU_TEXTS.get(language, MENU_TEXTS["uz"])
    
    builder = ReplyKeyboardBuilder()
    
    # Row 1: Catalog and Search
    builder.row(
        KeyboardButton(text=texts["catalog"]),
        KeyboardButton(text=texts["search"]),
    )
    
    # Row 2: Cart and Orders
    builder.row(
        KeyboardButton(text=texts["cart"]),
        KeyboardButton(text=texts["orders"]),
    )
    
    # Row 3: Profile and Help
    builder.row(
        KeyboardButton(text=texts["profile"]),
        KeyboardButton(text=texts["help"]),
    )
    
    return builder.as_markup(resize_keyboard=True)


def get_seller_menu_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get seller menu keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = SELLER_TEXTS.get(language, SELLER_TEXTS["uz"])
    
    builder = ReplyKeyboardBuilder()
    
    # Row 1: Dashboard and Products
    builder.row(
        KeyboardButton(text=texts["dashboard"]),
        KeyboardButton(text=texts["products"]),
    )
    
    # Row 2: Orders and Analytics
    builder.row(
        KeyboardButton(text=texts["orders"]),
        KeyboardButton(text=texts["analytics"]),
    )
    
    # Row 3: Settings and Back
    builder.row(
        KeyboardButton(text=texts["settings"]),
        KeyboardButton(text=texts["back"]),
    )
    
    return builder.as_markup(resize_keyboard=True)


def get_admin_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Get admin menu keyboard.
    
    Returns:
        ReplyKeyboardMarkup
    """
    builder = ReplyKeyboardBuilder()
    
    # Row 1
    builder.row(
        KeyboardButton(text="📊 Dashboard"),
        KeyboardButton(text="👥 Foydalanuvchilar"),
    )
    
    # Row 2
    builder.row(
        KeyboardButton(text="🏪 Sotuvchilar"),
        KeyboardButton(text="📦 Mahsulotlar"),
    )
    
    # Row 3
    builder.row(
        KeyboardButton(text="📋 Buyurtmalar"),
        KeyboardButton(text="📁 Kategoriyalar"),
    )
    
    # Row 4
    builder.row(
        KeyboardButton(text="📢 Xabar yuborish"),
        KeyboardButton(text="⚙️ Sozlamalar"),
    )
    
    # Row 5
    builder.row(
        KeyboardButton(text="⬅️ Asosiy menyu"),
    )
    
    return builder.as_markup(resize_keyboard=True)


# ==========================================
# Text constants for different languages
# ==========================================

MENU_TEXTS = {
    "uz": {
        "catalog": "🛍️ Katalog",
        "search": "🔍 Qidirish",
        "cart": "🛒 Savat",
        "orders": "📋 Buyurtmalar",
        "profile": "👤 Profil",
        "help": "❓ Yordam",
    },
    "ru": {
        "catalog": "🛍️ Каталог",
        "search": "🔍 Поиск",
        "cart": "🛒 Корзина",
        "orders": "📋 Заказы",
        "profile": "👤 Профиль",
        "help": "❓ Помощь",
    },
    "en": {
        "catalog": "🛍️ Catalog",
        "search": "🔍 Search",
        "cart": "🛒 Cart",
        "orders": "📋 Orders",
        "profile": "👤 Profile",
        "help": "❓ Help",
    },
}

SELLER_TEXTS = {
    "uz": {
        "dashboard": "📊 Dashboard",
        "products": "📦 Mahsulotlar",
        "orders": "📋 Buyurtmalar",
        "analytics": "📈 Statistika",
        "settings": "⚙️ Sozlamalar",
        "back": "⬅️ Orqaga",
    },
    "ru": {
        "dashboard": "📊 Панель",
        "products": "📦 Товары",
        "orders": "📋 Заказы",
        "analytics": "📈 Статистика",
        "settings": "⚙️ Настройки",
        "back": "⬅️ Назад",
    },
    "en": {
        "dashboard": "📊 Dashboard",
        "products": "📦 Products",
        "orders": "📋 Orders",
        "analytics": "📈 Analytics",
        "settings": "⚙️ Settings",
        "back": "⬅️ Back",
    },
}
