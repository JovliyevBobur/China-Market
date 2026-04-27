"""
🔔 Callback Data Module

Callback data factories for inline keyboards.
"""

from aiogram.filters.callback_data import CallbackData


# ==========================================
# Navigation
# ==========================================

class NavigationCallback(CallbackData, prefix="nav"):
    """Navigation callback data."""
    action: str
    data: str = ""


class MenuCallback(CallbackData, prefix="menu"):
    """Main menu callback data."""
    section: str


# ==========================================
# Catalog & Products
# ==========================================

class CatalogCallback(CallbackData, prefix="cat"):
    """Catalog browsing callback data."""
    action: str  # view, filter, sort
    category_id: int = 0
    page: int = 1


class ProductCallback(CallbackData, prefix="prod"):
    """Product actions callback data."""
    action: str  # view, add_cart, favorite, review
    product_id: int
    quantity: int = 1


class CategoryCallback(CallbackData, prefix="catg"):
    """Category selection callback data."""
    action: str  # select, back
    category_id: int


# ==========================================
# Cart
# ==========================================

class CartCallback(CallbackData, prefix="cart"):
    """Cart actions callback data."""
    action: str  # view, add, remove, update, clear, checkout
    product_id: int = 0
    quantity: int = 1


class CartItemCallback(CallbackData, prefix="cart_item"):
    """Cart item actions callback data."""
    action: str  # inc, dec, remove
    item_id: int


# ==========================================
# Orders
# ==========================================

class OrderCallback(CallbackData, prefix="order"):
    """Order actions callback data."""
    action: str  # view, cancel, track, rate, reorder
    order_id: int


class CheckoutCallback(CallbackData, prefix="checkout"):
    """Checkout process callback data."""
    step: str
    data: str = ""


class DeliveryCallback(CallbackData, prefix="delivery"):
    """Delivery selection callback data."""
    type: str  # pickup, standard, express


class PaymentCallback(CallbackData, prefix="payment"):
    """Payment method callback data."""
    method: str  # stars, click, payme, cash


# ==========================================
# User
# ==========================================

class ProfileCallback(CallbackData, prefix="profile"):
    """Profile actions callback data."""
    action: str  # view, edit, settings
    field: str = ""


class LanguageCallback(CallbackData, prefix="lang"):
    """Language selection callback data."""
    language: str  # uz, ru, en


class FavoriteCallback(CallbackData, prefix="fav"):
    """Favorites callback data."""
    action: str  # add, remove, view
    product_id: int = 0


# ==========================================
# Reviews
# ==========================================

class ReviewCallback(CallbackData, prefix="review"):
    """Review actions callback data."""
    action: str  # add, view, helpful
    product_id: int = 0
    review_id: int = 0


class RatingCallback(CallbackData, prefix="rating"):
    """Rating selection callback data."""
    rating: int  # 1-5


# ==========================================
# Seller
# ==========================================

class SellerCallback(CallbackData, prefix="seller"):
    """Seller dashboard callback data."""
    action: str
    data: int = 0


class SellerProductCallback(CallbackData, prefix="s_prod"):
    """Seller product management callback data."""
    action: str  # add, edit, delete, toggle
    product_id: int = 0


class SellerOrderCallback(CallbackData, prefix="s_order"):
    """Seller order management callback data."""
    action: str  # view, accept, reject, ship
    order_id: int


# ==========================================
# Admin
# ==========================================

class AdminCallback(CallbackData, prefix="admin"):
    """Admin panel callback data."""
    action: str
    data: int = 0


class UserManageCallback(CallbackData, prefix="a_user"):
    """Admin user management callback data."""
    action: str  # view, ban, unban, role
    user_id: int


class ModerationCallback(CallbackData, prefix="mod"):
    """Moderation callback data."""
    action: str  # approve, reject
    type: str  # product, seller
    id: int


class BroadcastCallback(CallbackData, prefix="bc"):
    """Broadcast callback data."""
    action: str
    data: str = ""


class CategoryManageCallback(CallbackData, prefix="a_cat"):
    """Admin category management callback data."""
    action: str  # add, edit, delete
    category_id: int = 0


# ==========================================
# Pagination
# ==========================================

class PaginationCallback(CallbackData, prefix="page"):
    """Pagination callback data."""
    action: str  # first, prev, next, last, goto
    page: int
    context: str  # What we're paginating


# ==========================================
# Common
# ==========================================

class ConfirmCallback(CallbackData, prefix="confirm"):
    """Confirmation callback data."""
    action: str  # yes, no
    context: str
    data: int = 0


class CancelCallback(CallbackData, prefix="cancel"):
    """Cancel action callback data."""
    context: str = "general"


class BackCallback(CallbackData, prefix="back"):
    """Back navigation callback data."""
    to: str
    data: int = 0


# ==========================================
# Support
# ==========================================

class SupportCallback(CallbackData, prefix="support"):
    """Support callback data."""
    action: str
    ticket_id: int = 0
