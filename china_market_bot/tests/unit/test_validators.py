"""
🧪 Validators Unit Tests
"""

import pytest
from decimal import Decimal

from app.utils.validators import (
    validate_phone,
    validate_email,
    validate_price,
    validate_quantity,
    sanitize_text,
    generate_slug,
)


class TestValidatePhone:
    """Tests for phone validation."""
    
    def test_valid_phone_with_plus(self):
        """Test valid phone with +998 prefix."""
        result = validate_phone("+998901234567")
        assert result == "+998901234567"
    
    def test_valid_phone_without_plus(self):
        """Test valid phone without + prefix."""
        result = validate_phone("998901234567")
        assert result == "+998901234567"
    
    def test_valid_phone_short(self):
        """Test valid short phone (9 digits)."""
        result = validate_phone("901234567")
        assert result == "+998901234567"
    
    def test_invalid_phone(self):
        """Test invalid phone number."""
        result = validate_phone("123456")
        assert result is None
    
    def test_phone_with_spaces(self):
        """Test phone with spaces."""
        result = validate_phone("+998 90 123 45 67")
        assert result == "+998901234567"


class TestValidateEmail:
    """Tests for email validation."""
    
    def test_valid_email(self):
        """Test valid email."""
        result = validate_email("test@example.com")
        assert result == "test@example.com"
    
    def test_valid_email_uppercase(self):
        """Test email normalization to lowercase."""
        result = validate_email("Test@Example.COM")
        assert result == "test@example.com"
    
    def test_invalid_email_no_at(self):
        """Test invalid email without @."""
        result = validate_email("testexample.com")
        assert result is None
    
    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        result = validate_email("test@")
        assert result is None


class TestValidatePrice:
    """Tests for price validation."""
    
    def test_valid_price(self):
        """Test valid price."""
        result = validate_price("100000")
        assert result == Decimal("100000.00")
    
    def test_valid_price_with_decimal(self):
        """Test valid price with decimal."""
        result = validate_price("99.99")
        assert result == Decimal("99.99")
    
    def test_valid_price_with_comma(self):
        """Test price with comma as decimal separator."""
        result = validate_price("99,99")
        assert result == Decimal("99.99")
    
    def test_valid_price_with_spaces(self):
        """Test price with thousand separators."""
        result = validate_price("100 000")
        assert result == Decimal("100000.00")
    
    def test_invalid_price_negative(self):
        """Test negative price."""
        result = validate_price("-100")
        assert result is None
    
    def test_invalid_price_text(self):
        """Test non-numeric price."""
        result = validate_price("abc")
        assert result is None


class TestValidateQuantity:
    """Tests for quantity validation."""
    
    def test_valid_quantity(self):
        """Test valid quantity."""
        result = validate_quantity("10")
        assert result == 10
    
    def test_invalid_quantity_zero(self):
        """Test zero quantity."""
        result = validate_quantity("0")
        assert result is None
    
    def test_invalid_quantity_negative(self):
        """Test negative quantity."""
        result = validate_quantity("-5")
        assert result is None
    
    def test_invalid_quantity_float(self):
        """Test float quantity."""
        result = validate_quantity("10.5")
        assert result is None


class TestSanitizeText:
    """Tests for text sanitization."""
    
    def test_remove_angle_brackets(self):
        """Test removing < and >."""
        result = sanitize_text("<script>alert('xss')</script>")
        assert "<" not in result
        assert ">" not in result
    
    def test_remove_quotes(self):
        """Test removing quotes."""
        result = sanitize_text('Test "quoted" text')
        assert '"' not in result
    
    def test_truncate_long_text(self):
        """Test truncating long text."""
        long_text = "a" * 10000
        result = sanitize_text(long_text)
        assert len(result) <= 5000


class TestGenerateSlug:
    """Tests for slug generation."""
    
    def test_basic_slug(self):
        """Test basic slug generation."""
        result = generate_slug("Hello World")
        assert result == "hello-world"
    
    def test_cyrillic_slug(self):
        """Test Cyrillic transliteration."""
        result = generate_slug("Привет мир")
        assert result == "privet-mir"
    
    def test_uzbek_slug(self):
        """Test Uzbek transliteration."""
        result = generate_slug("O'zbek tili")
        assert "uzbek" in result or "ozbek" in result
    
    def test_special_chars(self):
        """Test removing special characters."""
        result = generate_slug("Test! @#$% Product")
        assert result == "test-product"
    
    def test_multiple_spaces(self):
        """Test handling multiple spaces."""
        result = generate_slug("Test    Product")
        assert result == "test-product"
