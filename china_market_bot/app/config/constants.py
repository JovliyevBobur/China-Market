"""
📋 Global Constants Module

All application constants defined in one place.
"""

from enum import Enum, auto
from typing import Final


# ==========================================
# Bot Constants
# ==========================================
BOT_NAME: Final[str] = "🛒 China Market"
BOT_VERSION: Final[str] = "1.0.0"
SUPPORT_USERNAME: Final[str] = "@china_market_support"


# ==========================================
# Pagination Constants
# ==========================================
PRODUCTS_PER_PAGE: Final[int] = 10
ORDERS_PER_PAGE: Final[int] = 5
USERS_PER_PAGE: Final[int] = 20
REVIEWS_PER_PAGE: Final[int] = 5
CATEGORIES_PER_PAGE: Final[int] = 8


# ==========================================
# Limits Constants
# ==========================================
MAX_PRODUCT_NAME_LENGTH: Final[int] = 200
MAX_PRODUCT_DESCRIPTION_LENGTH: Final[int] = 5000
MAX_REVIEW_LENGTH: Final[int] = 1000
MAX_CART_ITEMS: Final[int] = 50
MAX_PRODUCT_IMAGES: Final[int] = 10
MIN_PRODUCT_PRICE: Final[float] = 1000  # 1000 so'm
MAX_PRODUCT_PRICE: Final[float] = 100_000_000_000  # 100 milliard so'm
MAX_PRODUCT_QUANTITY: Final[int] = 100_000


# ==========================================
# Media Constants
# ==========================================
ALLOWED_IMAGE_TYPES: Final[tuple] = ("image/jpeg", "image/png", "image/gif", "image/webp")
MAX_IMAGE_SIZE: Final[int] = 10 * 1024 * 1024  # 10MB
IMAGE_THUMBNAIL_SIZE: Final[tuple] = (300, 300)
IMAGE_PREVIEW_SIZE: Final[tuple] = (800, 800)


# ==========================================
# Time Constants (in seconds)
# ==========================================
CACHE_TTL_SHORT: Final[int] = 60  # 1 minute
CACHE_TTL_MEDIUM: Final[int] = 300  # 5 minutes
CACHE_TTL_LONG: Final[int] = 3600  # 1 hour
CACHE_TTL_DAY: Final[int] = 86400  # 24 hours

SESSION_EXPIRE: Final[int] = 86400 * 7  # 7 days
ORDER_TIMEOUT: Final[int] = 3600  # 1 hour for unpaid orders


# ==========================================
# Currency Constants
# ==========================================
CURRENCY_UZS: Final[str] = "UZS"
CURRENCY_USD: Final[str] = "USD"
CURRENCY_STARS: Final[str] = "XTR"  # Telegram Stars

DEFAULT_CURRENCY: Final[str] = CURRENCY_UZS
CURRENCY_SYMBOL: Final[str] = "so'm"


# ==========================================
# User Roles
# ==========================================
class UserRole(str, Enum):
    """User role enumeration."""
    USER = "user"
    SELLER = "seller"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


# ==========================================
# Order Status
# ==========================================
class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"           # Kutilmoqda
    CONFIRMED = "confirmed"       # Tasdiqlangan
    PROCESSING = "processing"     # Qayta ishlanmoqda
    SHIPPED = "shipped"           # Yuborilgan
    DELIVERED = "delivered"       # Yetkazilgan
    COMPLETED = "completed"       # Tugallangan
    CANCELLED = "cancelled"       # Bekor qilingan
    REFUNDED = "refunded"         # Qaytarilgan


ORDER_STATUS_EMOJI: dict[OrderStatus, str] = {
    OrderStatus.PENDING: "⏳",
    OrderStatus.CONFIRMED: "✅",
    OrderStatus.PROCESSING: "📦",
    OrderStatus.SHIPPED: "🚚",
    OrderStatus.DELIVERED: "📬",
    OrderStatus.COMPLETED: "🎉",
    OrderStatus.CANCELLED: "❌",
    OrderStatus.REFUNDED: "💸",
}


# ==========================================
# Payment Status
# ==========================================
class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# ==========================================
# Payment Methods
# ==========================================
class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    TELEGRAM_STARS = "telegram_stars"
    CLICK = "click"
    PAYME = "payme"
    CASH = "cash"


PAYMENT_METHOD_NAMES: dict[PaymentMethod, str] = {
    PaymentMethod.TELEGRAM_STARS: "⭐ Telegram Stars",
    PaymentMethod.CLICK: "💳 Click",
    PaymentMethod.PAYME: "💳 Payme",
    PaymentMethod.CASH: "💵 Naqd pul",
}


# ==========================================
# Moderation Status
# ==========================================
class ModerationStatus(str, Enum):
    """Moderation status for products and sellers."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


# ==========================================
# Delivery Types
# ==========================================
class DeliveryType(str, Enum):
    """Delivery type enumeration."""
    PICKUP = "pickup"       # O'zi olib ketadi
    STANDARD = "standard"   # Oddiy yetkazib berish
    EXPRESS = "express"     # Tez yetkazib berish


DELIVERY_TYPE_NAMES: dict[DeliveryType, str] = {
    DeliveryType.PICKUP: "🏪 O'zi olib ketadi",
    DeliveryType.STANDARD: "🚚 Oddiy yetkazib berish",
    DeliveryType.EXPRESS: "⚡ Tez yetkazib berish",
}


# ==========================================
# Language Codes
# ==========================================
class Language(str, Enum):
    """Supported languages."""
    UZ = "uz"
    RU = "ru"
    EN = "en"


LANGUAGE_NAMES: dict[Language, str] = {
    Language.UZ: "🇺🇿 O'zbek",
    Language.RU: "🇷🇺 Русский",
    Language.EN: "🇬🇧 English",
}


# ==========================================
# Rating Constants
# ==========================================
MIN_RATING: Final[int] = 1
MAX_RATING: Final[int] = 5
RATING_EMOJI: dict[int, str] = {
    1: "⭐",
    2: "⭐⭐",
    3: "⭐⭐⭐",
    4: "⭐⭐⭐⭐",
    5: "⭐⭐⭐⭐⭐",
}


# ==========================================
# Text Templates
# ==========================================
WELCOME_TEXT: Final[str] = """
🛒 <b>{bot_name}</b> ga xush kelibsiz!

Bu yerda siz:
• 📦 Mahsulotlarni ko'rishingiz
• 🔍 Qidiruv qilishingiz
• 🛒 Savatingizga qo'shishingiz
• 💳 Xarid qilishingiz mumkin!

Davom etish uchun quyidagi tugmalardan birini tanlang:
"""

HELP_TEXT: Final[str] = """
❓ <b>Yordam</b>

<b>Asosiy buyruqlar:</b>
/start - Botni ishga tushirish
/catalog - Mahsulotlar katalogi
/search - Mahsulot qidirish
/cart - Savat
/orders - Buyurtmalar tarixi
/profile - Profil
/help - Yordam

<b>Savol yoki muammo bo'lsa:</b>
{support_username}

<b>Telegram:</b> {support_username}
"""


# ==========================================
# Error Messages
# ==========================================
class ErrorMessages:
    """Error messages in Uzbek."""
    GENERAL_ERROR = "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
    NOT_FOUND = "❌ Topilmadi."
    UNAUTHORIZED = "🔒 Sizda bu amalni bajarishga ruxsat yo'q."
    BANNED = "🚫 Sizning hisobingiz bloklangan."
    THROTTLED = "⏳ Juda ko'p so'rov. Biroz kuting."
    INVALID_INPUT = "❌ Noto'g'ri ma'lumot kiritildi."
    PRODUCT_NOT_FOUND = "❌ Mahsulot topilmadi."
    CATEGORY_NOT_FOUND = "❌ Kategoriya topilmadi."
    ORDER_NOT_FOUND = "❌ Buyurtma topilmadi."
    CART_EMPTY = "🛒 Savatingiz bo'sh."
    INSUFFICIENT_STOCK = "❌ Yetarli mahsulot mavjud emas."
    PAYMENT_FAILED = "❌ To'lov amalga oshmadi."


# ==========================================
# Success Messages
# ==========================================
class SuccessMessages:
    """Success messages in Uzbek."""
    ADDED_TO_CART = "✅ Mahsulot savatga qo'shildi!"
    REMOVED_FROM_CART = "✅ Mahsulot savatdan o'chirildi!"
    ORDER_CREATED = "✅ Buyurtmangiz qabul qilindi!"
    PAYMENT_SUCCESS = "✅ To'lov muvaffaqiyatli amalga oshirildi!"
    PROFILE_UPDATED = "✅ Profilingiz yangilandi!"
    PRODUCT_ADDED = "✅ Mahsulot qo'shildi!"
    PRODUCT_UPDATED = "✅ Mahsulot yangilandi!"
    PRODUCT_DELETED = "✅ Mahsulot o'chirildi!"
    REVIEW_ADDED = "✅ Sharhingiz qo'shildi!"
