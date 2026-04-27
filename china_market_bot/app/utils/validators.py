"""
✅ Validators Module

Input validation utilities.
"""

import re
from typing import Optional
from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, Field, field_validator


# ==========================================
# Regular Expressions
# ==========================================

PHONE_REGEX = re.compile(r"^\+?998[0-9]{9}$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
SLUG_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DANGEROUS_CHARS = re.compile(r"[<>\"';()&]")


# ==========================================
# Validation Functions
# ==========================================

def validate_phone(phone: str) -> Optional[str]:
    """
    Validate and normalize phone number.
    
    Args:
        phone: Phone number string
    
    Returns:
        Normalized phone or None if invalid
    """
    # Remove spaces and dashes
    phone = phone.replace(" ", "").replace("-", "")
    
    # Add country code if missing
    if phone.startswith("998"):
        phone = f"+{phone}"
    elif phone.startswith("9") and len(phone) == 9:
        phone = f"+998{phone}"
    
    if PHONE_REGEX.match(phone):
        return phone
    
    return None


def validate_email(email: str) -> Optional[str]:
    """
    Validate email address.
    
    Args:
        email: Email address
    
    Returns:
        Normalized email or None if invalid
    """
    email = email.strip().lower()
    
    if EMAIL_REGEX.match(email):
        return email
    
    return None


def validate_username(username: str) -> Optional[str]:
    """
    Validate username.
    
    Args:
        username: Username string
    
    Returns:
        Normalized username or None if invalid
    """
    username = username.strip().lower()
    
    if USERNAME_REGEX.match(username):
        return username
    
    return None


def validate_price(price: str) -> Optional[Decimal]:
    """
    Validate and parse price.
    
    Args:
        price: Price string
    
    Returns:
        Decimal price or None if invalid
    """
    try:
        # Remove spaces and replace comma with dot
        price = price.replace(" ", "").replace(",", ".")
        
        value = Decimal(price)
        
        if value <= 0:
            return None
        
        return value.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return None


def validate_quantity(quantity: str) -> Optional[int]:
    """
    Validate quantity.
    
    Args:
        quantity: Quantity string
    
    Returns:
        Integer quantity or None if invalid
    """
    try:
        value = int(quantity)
        
        if value <= 0:
            return None
        
        return value
    except ValueError:
        return None


def sanitize_text(text: str) -> str:
    """
    Sanitize text input by removing dangerous characters.
    
    Args:
        text: Input text
    
    Returns:
        Sanitized text
    """
    # Remove dangerous characters
    text = DANGEROUS_CHARS.sub("", text)
    
    # Limit length
    text = text[:5000]
    
    return text.strip()


def sanitize_html(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: Input text with potential HTML
    
    Returns:
        Text without HTML tags
    """
    return re.sub(r"<[^>]+>", "", text)


def generate_slug(text: str) -> str:
    """
    Generate URL-friendly slug from text.
    
    Args:
        text: Input text
    
    Returns:
        URL-friendly slug
    """
    # Transliteration map for Cyrillic
    translit_map = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
        "е": "e", "ё": "yo", "ж": "zh", "з": "z", "и": "i",
        "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
        "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch",
        "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya",
        "ў": "o", "қ": "q", "ғ": "g", "ҳ": "h",
    }
    
    text = text.lower()
    
    # Transliterate
    result = ""
    for char in text:
        result += translit_map.get(char, char)
    
    # Replace spaces with hyphens
    result = re.sub(r"\s+", "-", result)
    
    # Remove non-alphanumeric except hyphens
    result = re.sub(r"[^a-z0-9-]", "", result)
    
    # Remove multiple hyphens
    result = re.sub(r"-+", "-", result)
    
    # Remove leading/trailing hyphens
    result = result.strip("-")
    
    return result[:300]


# ==========================================
# Pydantic Schemas for Validation
# ==========================================

class ProductCreateSchema(BaseModel):
    """Product creation validation schema."""
    
    name: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    price: Decimal = Field(..., gt=0, le=100_000_000_000)
    quantity: int = Field(..., ge=0, le=100_000)
    category_id: int = Field(..., gt=0)
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate product name."""
        if DANGEROUS_CHARS.search(v):
            raise ValueError("Noto'g'ri belgilar aniqlandi")
        return v.strip()
    
    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Validate and sanitize description."""
        return sanitize_html(v.strip())


class UserUpdateSchema(BaseModel):
    """User update validation schema."""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=200)
    last_name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> Optional[str]:
        """Validate phone number."""
        if v is None:
            return None
        result = validate_phone(v)
        if result is None:
            raise ValueError("Noto'g'ri telefon raqami")
        return result
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> Optional[str]:
        """Validate email."""
        if v is None:
            return None
        result = validate_email(v)
        if result is None:
            raise ValueError("Noto'g'ri email manzil")
        return result


class OrderCreateSchema(BaseModel):
    """Order creation validation schema."""
    
    customer_name: str = Field(..., min_length=2, max_length=200)
    customer_phone: str = Field(..., max_length=20)
    delivery_type: str = Field(...)
    payment_method: str = Field(...)
    delivery_address: Optional[str] = Field(None, max_length=500)
    customer_notes: Optional[str] = Field(None, max_length=1000)
    
    @field_validator("customer_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number."""
        result = validate_phone(v)
        if result is None:
            raise ValueError("Noto'g'ri telefon raqami")
        return result
