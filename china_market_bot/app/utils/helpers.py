"""
🛠️ Helper Functions Module

General purpose helper functions.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Callable, Awaitable, TypeVar, Optional

T = TypeVar("T")


def generate_uuid() -> str:
    """
    Generate UUID string.
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """
    Generate short unique ID.
    
    Args:
        length: ID length
    
    Returns:
        Short ID string
    """
    return uuid.uuid4().hex[:length].upper()


def generate_order_number() -> str:
    """
    Generate unique order number.
    
    Returns:
        Order number string
    """
    now = datetime.utcnow()
    unique_id = uuid.uuid4().hex[:8].upper()
    return f"ORD-{now.strftime('%Y%m%d')}-{unique_id}"


def chunks(lst: list, n: int):
    """
    Split list into chunks.
    
    Args:
        lst: Input list
        n: Chunk size
    
    Yields:
        List chunks
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def flatten(lst: list) -> list:
    """
    Flatten nested list.
    
    Args:
        lst: Nested list
    
    Returns:
        Flat list
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def unique(lst: list) -> list:
    """
    Get unique items preserving order.
    
    Args:
        lst: Input list
    
    Returns:
        List with unique items
    """
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


def safe_get(
    dictionary: dict,
    *keys,
    default: Any = None,
) -> Any:
    """
    Safely get nested dictionary value.
    
    Args:
        dictionary: Input dictionary
        *keys: Keys path
        default: Default value
    
    Returns:
        Value or default
    """
    for key in keys:
        try:
            dictionary = dictionary[key]
        except (KeyError, TypeError, IndexError):
            return default
    return dictionary


def merge_dicts(*dicts: dict) -> dict:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
    
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


async def run_with_timeout(
    coro: Awaitable[T],
    timeout: float,
    default: T = None,
) -> T:
    """
    Run coroutine with timeout.
    
    Args:
        coro: Coroutine to run
        timeout: Timeout in seconds
        default: Default value on timeout
    
    Returns:
        Coroutine result or default
    """
    try:
        return await asyncio.wait_for(coro, timeout)
    except asyncio.TimeoutError:
        return default


async def retry(
    func: Callable[..., Awaitable[T]],
    *args,
    retries: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (Exception,),
    **kwargs,
) -> Optional[T]:
    """
    Retry async function with delay.
    
    Args:
        func: Async function to retry
        *args: Function arguments
        retries: Number of retries
        delay: Delay between retries
        exceptions: Exceptions to catch
        **kwargs: Function keyword arguments
    
    Returns:
        Function result or None
    """
    last_exception = None
    
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            last_exception = e
            if attempt < retries - 1:
                await asyncio.sleep(delay * (attempt + 1))
    
    return None


def remove_none(d: dict) -> dict:
    """
    Remove None values from dictionary.
    
    Args:
        d: Input dictionary
    
    Returns:
        Dictionary without None values
    """
    return {k: v for k, v in d.items() if v is not None}


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between min and max.
    
    Args:
        value: Input value
        min_val: Minimum value
        max_val: Maximum value
    
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def calculate_discount_percent(
    original_price: float,
    discounted_price: float,
) -> int:
    """
    Calculate discount percentage.
    
    Args:
        original_price: Original price
        discounted_price: Discounted price
    
    Returns:
        Discount percentage
    """
    if original_price <= 0:
        return 0
    
    discount = ((original_price - discounted_price) / original_price) * 100
    
    return int(discount)


def get_pagination_info(
    total: int,
    page: int,
    per_page: int,
) -> dict:
    """
    Calculate pagination info.
    
    Args:
        total: Total items count
        page: Current page
        per_page: Items per page
    
    Returns:
        Pagination info dictionary
    """
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    
    # Ensure page is valid
    page = max(1, min(page, total_pages))
    
    offset = (page - 1) * per_page
    
    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "offset": offset,
        "has_prev": page > 1,
        "has_next": page < total_pages,
    }


def mask_phone(phone: str) -> str:
    """
    Mask phone number for display.
    
    Args:
        phone: Phone number
    
    Returns:
        Masked phone (e.g., +998 ** *** ** 12)
    """
    if len(phone) < 4:
        return phone
    
    return phone[:7] + " ** *** ** " + phone[-2:]


def mask_email(email: str) -> str:
    """
    Mask email for display.
    
    Args:
        email: Email address
    
    Returns:
        Masked email (e.g., u***@example.com)
    """
    if "@" not in email:
        return email
    
    parts = email.split("@")
    username = parts[0]
    domain = parts[1]
    
    if len(username) <= 1:
        masked = username
    else:
        masked = username[0] + "*" * min(3, len(username) - 1)
    
    return f"{masked}@{domain}"
