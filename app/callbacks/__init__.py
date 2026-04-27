"""
🔔 Callbacks Package

Callback data factories for inline keyboards.
"""

from .callback_data import (
    AdminCallback,
    BackCallback,
    BroadcastCallback,
    CancelCallback,
    CartCallback,
    CartItemCallback,
    CatalogCallback,
    CategoryCallback,
    CategoryManageCallback,
    CheckoutCallback,
    ConfirmCallback,
    DeliveryCallback,
    FavoriteCallback,
    LanguageCallback,
    MenuCallback,
    ModerationCallback,
    NavigationCallback,
    OrderCallback,
    PaginationCallback,
    PaymentCallback,
    ProductCallback,
    ProfileCallback,
    RatingCallback,
    ReviewCallback,
    SellerCallback,
    SellerOrderCallback,
    SellerProductCallback,
    SupportCallback,
    UserManageCallback,
)

__all__ = [
    # Navigation
    "NavigationCallback",
    "MenuCallback",
    "BackCallback",
    "CancelCallback",
    "ConfirmCallback",
    "PaginationCallback",
    # Catalog
    "CatalogCallback",
    "ProductCallback",
    "CategoryCallback",
    # Cart
    "CartCallback",
    "CartItemCallback",
    # Orders
    "OrderCallback",
    "CheckoutCallback",
    "DeliveryCallback",
    "PaymentCallback",
    # User
    "ProfileCallback",
    "LanguageCallback",
    "FavoriteCallback",
    # Reviews
    "ReviewCallback",
    "RatingCallback",
    # Seller
    "SellerCallback",
    "SellerProductCallback",
    "SellerOrderCallback",
    # Admin
    "AdminCallback",
    "UserManageCallback",
    "ModerationCallback",
    "BroadcastCallback",
    "CategoryManageCallback",
    # Support
    "SupportCallback",
]
