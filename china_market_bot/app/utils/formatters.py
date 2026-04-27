"""
📝 Formatters Module

Text formatting utilities.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional


def format_price(
    price: Decimal | float | int,
    currency: str = "so'm",
    show_currency: bool = True,
) -> str:
    """
    Format price for display.
    
    Args:
        price: Price value
        currency: Currency name
        show_currency: Whether to show currency
    
    Returns:
        Formatted price string
    """
    # Convert to decimal
    if isinstance(price, (float, int)):
        price = Decimal(str(price))
    
    # Format with thousands separator
    formatted = f"{price:,.0f}".replace(",", " ")
    
    if show_currency:
        return f"{formatted} {currency}"
    
    return formatted


def format_phone(phone: str) -> str:
    """
    Format phone number for display.
    
    Args:
        phone: Phone number string
    
    Returns:
        Formatted phone string
    """
    # Remove all non-digits
    digits = "".join(filter(str.isdigit, phone))
    
    if len(digits) == 12:
        # +998 XX XXX XX XX
        return f"+{digits[:3]} {digits[3:5]} {digits[5:8]} {digits[8:10]} {digits[10:12]}"
    elif len(digits) == 9:
        # XX XXX XX XX
        return f"{digits[:2]} {digits[2:5]} {digits[5:7]} {digits[7:9]}"
    
    return phone


def format_date(
    dt: datetime | date,
    include_time: bool = False,
    language: str = "uz",
) -> str:
    """
    Format date for display.
    
    Args:
        dt: Date or datetime
        include_time: Include time
        language: Language code
    
    Returns:
        Formatted date string
    """
    if isinstance(dt, datetime):
        d = dt.date()
        t = dt.time()
    else:
        d = dt
        t = None
    
    # Month names
    months = {
        "uz": [
            "yanvar", "fevral", "mart", "aprel", "may", "iyun",
            "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"
        ],
        "ru": [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ],
        "en": [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
    }
    
    month = months.get(language, months["uz"])[d.month - 1]
    
    result = f"{d.day} {month} {d.year}"
    
    if include_time and t:
        result += f", {t.strftime('%H:%M')}"
    
    return result


def format_datetime_short(dt: datetime) -> str:
    """
    Format datetime in short format.
    
    Args:
        dt: Datetime
    
    Returns:
        Short formatted string
    """
    return dt.strftime("%d.%m.%Y %H:%M")


def format_time_ago(dt: datetime, language: str = "uz") -> str:
    """
    Format datetime as time ago.
    
    Args:
        dt: Datetime
        language: Language code
    
    Returns:
        Time ago string (e.g., "5 daqiqa oldin")
    """
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    
    texts = {
        "uz": {
            "now": "hozirgina",
            "minutes": "daqiqa oldin",
            "hours": "soat oldin",
            "days": "kun oldin",
        },
        "ru": {
            "now": "только что",
            "minutes": "минут назад",
            "hours": "часов назад",
            "days": "дней назад",
        },
        "en": {
            "now": "just now",
            "minutes": "minutes ago",
            "hours": "hours ago",
            "days": "days ago",
        },
    }
    
    t = texts.get(language, texts["uz"])
    
    if seconds < 60:
        return t["now"]
    elif minutes < 60:
        return f"{minutes} {t['minutes']}"
    elif hours < 24:
        return f"{hours} {t['hours']}"
    else:
        return f"{days} {t['days']}"


def format_quantity(
    quantity: int,
    unit: str = "dona",
    language: str = "uz",
) -> str:
    """
    Format quantity with proper pluralization.
    
    Args:
        quantity: Quantity number
        unit: Unit name
        language: Language code
    
    Returns:
        Formatted quantity string
    """
    return f"{quantity} {unit}"


def format_rating(rating: float, show_count: bool = False, count: int = 0) -> str:
    """
    Format rating with stars.
    
    Args:
        rating: Rating value (0-5)
        show_count: Show review count
        count: Review count
    
    Returns:
        Rating string with stars
    """
    # Full and empty stars
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    result = "⭐" * full_stars + "✨" * half_star + "☆" * empty_stars
    result += f" {rating:.1f}"
    
    if show_count:
        result += f" ({count})"
    
    return result


def format_order_number(order_number: str) -> str:
    """
    Format order number for display.
    
    Args:
        order_number: Order number
    
    Returns:
        Formatted order number
    """
    return f"#{order_number}"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size for display.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Human-readable size string
    """
    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    
    return f"{size:.1f} {units[unit_index]}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format percentage.
    
    Args:
        value: Value (0-100 or 0-1)
        decimals: Decimal places
    
    Returns:
        Percentage string
    """
    if value <= 1:
        value *= 100
    
    return f"{value:.{decimals}f}%"


def truncate_text(
    text: str,
    max_length: int = 100,
    suffix: str = "...",
) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].rsplit(" ", 1)[0] + suffix


def format_list(
    items: list,
    separator: str = ", ",
    last_separator: str = " va ",
) -> str:
    """
    Format list as text.
    
    Args:
        items: List of items
        separator: Separator between items
        last_separator: Separator before last item
    
    Returns:
        Formatted string
    """
    if not items:
        return ""
    
    if len(items) == 1:
        return str(items[0])
    
    if len(items) == 2:
        return f"{items[0]}{last_separator}{items[1]}"
    
    return separator.join(str(i) for i in items[:-1]) + last_separator + str(items[-1])
