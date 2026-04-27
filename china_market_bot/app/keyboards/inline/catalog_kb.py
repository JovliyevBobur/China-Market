"""
🛍️ Catalog Keyboards Module

Inline keyboards for catalog browsing.
"""

from typing import List, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks import (
    CatalogCallback,
    CategoryCallback,
    ProductCallback,
    CartCallback,
    FavoriteCallback,
    BackCallback,
)
from app.database.models import Category, Product


def get_categories_keyboard(
    categories: List[Category],
    parent_id: Optional[int] = None,
    show_back: bool = False,
) -> InlineKeyboardMarkup:
    """
    Get categories keyboard.
    
    Args:
        categories: List of categories
        parent_id: Parent category ID (for subcategories)
        show_back: Show back button
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    for category in categories:
        icon = category.icon or "📁"
        count = category.product_count
        
        builder.button(
            text=f"{icon} {category.name} ({count})",
            callback_data=CategoryCallback(
                action="select",
                category_id=category.id,
            ).pack(),
        )
    
    # Adjust to 2 columns
    builder.adjust(2)
    
    if show_back and parent_id:
        builder.row()
        builder.button(
            text="⬅️ Orqaga",
            callback_data=CategoryCallback(
                action="back",
                category_id=parent_id,
            ).pack(),
        )
    elif show_back:
        builder.row()
        builder.button(
            text="🏠 Asosiy menyu",
            callback_data=BackCallback(to="main").pack(),
        )
    
    return builder.as_markup()


def get_products_keyboard(
    products: List[Product],
    category_id: int,
    page: int = 1,
    total_pages: int = 1,
) -> InlineKeyboardMarkup:
    """
    Get products list keyboard.
    
    Args:
        products: List of products
        category_id: Current category ID
        page: Current page
        total_pages: Total pages
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    for product in products:
        # Format price
        price = f"{product.current_price:,.0f}".replace(",", " ")
        
        # Show discount badge
        if product.has_discount:
            text = f"🏷️ {product.name[:25]}... - {price} so'm"
        else:
            text = f"📦 {product.name[:25]}... - {price} so'm"
        
        # Determine redirect URL
        if getattr(product, "external_url", None):
            url = product.external_url
        else:
            from app.config import settings
            url = f"{settings.webapp_url}/product/{getattr(product, 'slug', product.id)}"
            
        builder.button(
            text=text,
            url=url,
        )
    
    # 1 product per row
    builder.adjust(1)
    
    # Pagination row
    if total_pages > 1:
        builder.row()
        
        if page > 1:
            builder.button(
                text="◀️",
                callback_data=CatalogCallback(
                    action="view",
                    category_id=category_id,
                    page=page - 1,
                ).pack(),
            )
        
        builder.button(
            text=f"{page}/{total_pages}",
            callback_data="noop",
        )
        
        if page < total_pages:
            builder.button(
                text="▶️",
                callback_data=CatalogCallback(
                    action="view",
                    category_id=category_id,
                    page=page + 1,
                ).pack(),
            )
    
    # Navigation row
    builder.row()
    builder.button(
        text="⬅️ Kategoriyalar",
        callback_data=CategoryCallback(
            action="back",
            category_id=0,
        ).pack(),
    )
    
    return builder.as_markup()


def get_product_keyboard(
    product: Product,
    quantity: int = 1,
    in_cart: bool = False,
    in_favorites: bool = False,
) -> InlineKeyboardMarkup:
    """
    Get product detail keyboard.
    
    Args:
        product: Product model
        quantity: Selected quantity
        in_cart: Is product in cart
        in_favorites: Is product in favorites
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Quantity selector
    builder.row()
    builder.button(
        text="➖",
        callback_data=ProductCallback(
            action="qty_dec",
            product_id=product.id,
            quantity=max(1, quantity - 1),
        ).pack(),
    )
    builder.button(
        text=f"📦 {quantity} dona",
        callback_data="noop",
    )
    builder.button(
        text="➕",
        callback_data=ProductCallback(
            action="qty_inc",
            product_id=product.id,
            quantity=min(product.available_quantity, quantity + 1),
        ).pack(),
    )
    
    # Add to cart button
    builder.row()
    if in_cart:
        builder.button(
            text="✅ Savatda",
            callback_data=CartCallback(action="view").pack(),
        )
    else:
        builder.button(
            text="🛒 Savatga qo'shish",
            callback_data=CartCallback(
                action="add",
                product_id=product.id,
                quantity=quantity,
            ).pack(),
        )
    
    # Favorites and reviews
    builder.row()
    if in_favorites:
        builder.button(
            text="💔 Sevimlilardan o'chirish",
            callback_data=FavoriteCallback(
                action="remove",
                product_id=product.id,
            ).pack(),
        )
    else:
        builder.button(
            text="❤️ Sevimlilarga",
            callback_data=FavoriteCallback(
                action="add",
                product_id=product.id,
            ).pack(),
        )
    
    builder.button(
        text=f"⭐ Sharhlar ({product.review_count})",
        callback_data=ProductCallback(
            action="reviews",
            product_id=product.id,
        ).pack(),
    )
    
    # Back button
    builder.row()
    builder.button(
        text="⬅️ Orqaga",
        callback_data=CatalogCallback(
            action="view",
            category_id=product.category_id or 0,
        ).pack(),
    )
    
    return builder.as_markup()


def get_search_filters_keyboard(
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "popular",
) -> InlineKeyboardMarkup:
    """
    Get search filters keyboard.
    
    Args:
        category_id: Selected category
        min_price: Minimum price filter
        max_price: Maximum price filter
        sort_by: Sort option
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    # Category filter
    cat_text = "📁 Kategoriya" if not category_id else "📁 Kategoriya ✓"
    builder.button(
        text=cat_text,
        callback_data=CatalogCallback(action="filter_category", category_id=0).pack(),
    )
    
    # Price filter
    price_text = "💰 Narx" if not (min_price or max_price) else "💰 Narx ✓"
    builder.button(
        text=price_text,
        callback_data=CatalogCallback(action="filter_price", category_id=0).pack(),
    )
    
    builder.adjust(2)
    
    # Sort options
    builder.row()
    sort_options = [
        ("🔥 Ommabop", "popular"),
        ("🆕 Yangi", "new"),
        ("💲 Arzon", "price_asc"),
        ("💎 Qimmat", "price_desc"),
    ]
    
    for text, sort_value in sort_options:
        if sort_by == sort_value:
            text = f"✅ {text}"
        builder.button(
            text=text,
            callback_data=CatalogCallback(action=f"sort_{sort_value}", category_id=0).pack(),
        )
    
    builder.adjust(2)
    
    # Clear filters
    builder.row()
    builder.button(
        text="🗑️ Filtrlarni tozalash",
        callback_data=CatalogCallback(action="clear_filters", category_id=0).pack(),
    )
    
    return builder.as_markup()
