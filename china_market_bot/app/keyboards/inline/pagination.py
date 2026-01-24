"""
📄 Pagination Keyboards Module

Pagination keyboard utilities.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks import PaginationCallback


def get_pagination_keyboard(
    current_page: int,
    total_pages: int,
    context: str,
    buttons_count: int = 5,
) -> InlineKeyboardMarkup:
    """
    Get pagination keyboard.
    
    Args:
        current_page: Current page (1-indexed)
        total_pages: Total number of pages
        context: Context identifier for callback
        buttons_count: Number of page buttons to show
    
    Returns:
        InlineKeyboardMarkup
    """
    if total_pages <= 1:
        return None
    
    builder = InlineKeyboardBuilder()
    buttons = []
    
    # First page button
    if current_page > 2:
        buttons.append(
            InlineKeyboardButton(
                text="⏮️ 1",
                callback_data=PaginationCallback(
                    action="goto",
                    page=1,
                    context=context,
                ).pack(),
            )
        )
    
    # Previous page button
    if current_page > 1:
        buttons.append(
            InlineKeyboardButton(
                text=f"◀️ {current_page - 1}",
                callback_data=PaginationCallback(
                    action="prev",
                    page=current_page - 1,
                    context=context,
                ).pack(),
            )
        )
    
    # Current page
    buttons.append(
        InlineKeyboardButton(
            text=f"· {current_page} ·",
            callback_data="noop",
        )
    )
    
    # Next page button
    if current_page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text=f"{current_page + 1} ▶️",
                callback_data=PaginationCallback(
                    action="next",
                    page=current_page + 1,
                    context=context,
                ).pack(),
            )
        )
    
    # Last page button
    if current_page < total_pages - 1:
        buttons.append(
            InlineKeyboardButton(
                text=f"{total_pages} ⏭️",
                callback_data=PaginationCallback(
                    action="goto",
                    page=total_pages,
                    context=context,
                ).pack(),
            )
        )
    
    builder.row(*buttons)
    
    return builder.as_markup()


def get_simple_pagination_keyboard(
    current_page: int,
    total_pages: int,
    context: str,
) -> InlineKeyboardMarkup:
    """
    Get simple pagination keyboard (prev/next only).
    
    Args:
        current_page: Current page
        total_pages: Total pages
        context: Context identifier
    
    Returns:
        InlineKeyboardMarkup
    """
    if total_pages <= 1:
        return None
    
    builder = InlineKeyboardBuilder()
    
    if current_page > 1:
        builder.button(
            text="◀️ Oldingi",
            callback_data=PaginationCallback(
                action="prev",
                page=current_page - 1,
                context=context,
            ).pack(),
        )
    
    builder.button(
        text=f"{current_page}/{total_pages}",
        callback_data="noop",
    )
    
    if current_page < total_pages:
        builder.button(
            text="Keyingi ▶️",
            callback_data=PaginationCallback(
                action="next",
                page=current_page + 1,
                context=context,
            ).pack(),
        )
    
    return builder.as_markup()


def get_numbered_pagination_keyboard(
    current_page: int,
    total_pages: int,
    context: str,
    visible_pages: int = 5,
) -> InlineKeyboardMarkup:
    """
    Get numbered pagination keyboard.
    
    Args:
        current_page: Current page
        total_pages: Total pages
        context: Context identifier
        visible_pages: Number of visible page numbers
    
    Returns:
        InlineKeyboardMarkup
    """
    if total_pages <= 1:
        return None
    
    builder = InlineKeyboardBuilder()
    
    # Calculate visible page range
    half = visible_pages // 2
    start_page = max(1, current_page - half)
    end_page = min(total_pages, start_page + visible_pages - 1)
    
    if end_page - start_page < visible_pages - 1:
        start_page = max(1, end_page - visible_pages + 1)
    
    # Previous button
    if current_page > 1:
        builder.button(
            text="◀️",
            callback_data=PaginationCallback(
                action="prev",
                page=current_page - 1,
                context=context,
            ).pack(),
        )
    
    # Page numbers
    for page in range(start_page, end_page + 1):
        if page == current_page:
            text = f"[{page}]"
        else:
            text = str(page)
        
        builder.button(
            text=text,
            callback_data=PaginationCallback(
                action="goto",
                page=page,
                context=context,
            ).pack(),
        )
    
    # Next button
    if current_page < total_pages:
        builder.button(
            text="▶️",
            callback_data=PaginationCallback(
                action="next",
                page=current_page + 1,
                context=context,
            ).pack(),
        )
    
    return builder.as_markup()


def add_pagination_row(
    builder: InlineKeyboardBuilder,
    current_page: int,
    total_pages: int,
    context: str,
) -> None:
    """
    Add pagination row to existing keyboard builder.
    
    Args:
        builder: Keyboard builder
        current_page: Current page
        total_pages: Total pages
        context: Context identifier
    """
    if total_pages <= 1:
        return
    
    builder.row()
    
    if current_page > 1:
        builder.button(
            text="◀️",
            callback_data=PaginationCallback(
                action="prev",
                page=current_page - 1,
                context=context,
            ).pack(),
        )
    
    builder.button(
        text=f"{current_page}/{total_pages}",
        callback_data="noop",
    )
    
    if current_page < total_pages:
        builder.button(
            text="▶️",
            callback_data=PaginationCallback(
                action="next",
                page=current_page + 1,
                context=context,
            ).pack(),
        )
