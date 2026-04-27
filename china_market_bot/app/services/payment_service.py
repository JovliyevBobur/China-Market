"""
💳 Payment Service Module

Service for payment processing.
"""

import base64
import hashlib
from decimal import Decimal
from typing import Optional
import uuid

from aiogram import Bot
from aiogram.types import LabeledPrice
from loguru import logger

from app.config import settings


class PaymentService:
    """
    Service for handling payments.
    """
    
    def __init__(self, bot: Bot):
        """
        Initialize payment service.
        
        Args:
            bot: Bot instance
        """
        self.bot = bot
    
    async def create_stars_invoice(
        self,
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        amount: int,
        photo_url: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create Telegram Stars invoice.
        
        Args:
            chat_id: User chat ID
            title: Invoice title
            description: Invoice description
            payload: Custom payload
            amount: Amount in Stars
            photo_url: Product photo URL
        
        Returns:
            Invoice link or None
        """
        try:
            prices = [
                LabeledPrice(label=title, amount=amount)
            ]
            
            invoice_link = await self.bot.create_invoice_link(
                title=title,
                description=description[:255] if len(description) > 255 else description,
                payload=payload,
                currency="XTR",  # Telegram Stars
                prices=prices,
                photo_url=photo_url,
                photo_width=512 if photo_url else None,
                photo_height=512 if photo_url else None,
            )
            
            return invoice_link
            
        except Exception as e:
            logger.error(f"Failed to create Stars invoice: {e}")
            return None
    
    async def send_stars_invoice(
        self,
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        amount: int,
        photo_url: Optional[str] = None,
    ) -> bool:
        """
        Send Telegram Stars invoice directly.
        
        Args:
            chat_id: User chat ID
            title: Invoice title
            description: Invoice description
            payload: Custom payload
            amount: Amount in Stars
            photo_url: Product photo URL
        
        Returns:
            True if sent successfully
        """
        try:
            prices = [
                LabeledPrice(label=title, amount=amount)
            ]
            
            await self.bot.send_invoice(
                chat_id=chat_id,
                title=title,
                description=description[:255] if len(description) > 255 else description,
                payload=payload,
                currency="XTR",
                prices=prices,
                photo_url=photo_url,
                photo_width=512 if photo_url else None,
                photo_height=512 if photo_url else None,
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Stars invoice: {e}")
            return False


class PaymeService:
    """
    Payme payment integration.
    """
    
    def __init__(
        self,
        merchant_id: str = None,
        secret_key: str = None,
        test_mode: bool = True,
    ):
        """
        Initialize Payme service.
        
        Args:
            merchant_id: Payme merchant ID
            secret_key: Payme secret key
            test_mode: Use test mode
        """
        self.merchant_id = merchant_id or settings.payme_merchant_id
        self.secret_key = secret_key or settings.payme_secret_key
        self.test_mode = test_mode if test_mode is not None else settings.payme_test_mode
        
        self.base_url = (
            "https://test.paycom.uz" if self.test_mode
            else "https://checkout.paycom.uz"
        )
    
    def generate_payment_url(
        self,
        order_id: str,
        amount: Decimal,
        return_url: Optional[str] = None,
    ) -> str:
        """
        Generate Payme payment URL.
        
        Args:
            order_id: Order ID
            amount: Amount in UZS (will be converted to tiyin)
            return_url: URL to return after payment
        
        Returns:
            Payment URL
        """
        # Convert to tiyin (1 so'm = 100 tiyin)
        amount_tiyin = int(amount * 100)
        
        # Build params string
        params = f"m={self.merchant_id}"
        params += f";ac.order_id={order_id}"
        params += f";a={amount_tiyin}"
        
        if return_url:
            params += f";c={return_url}"
        
        # Encode params
        encoded = base64.b64encode(params.encode()).decode()
        
        return f"{self.base_url}/{encoded}"
    
    def verify_callback(
        self,
        data: dict,
    ) -> bool:
        """
        Verify Payme callback signature.
        
        Args:
            data: Callback data from Payme
        
        Returns:
            True if valid
        """
        # Implementation depends on Payme API version
        # This is a placeholder
        return True


class ClickService:
    """
    Click payment integration.
    """
    
    def __init__(
        self,
        merchant_id: str = None,
        service_id: str = None,
        secret_key: str = None,
        test_mode: bool = True,
    ):
        """
        Initialize Click service.
        
        Args:
            merchant_id: Click merchant ID
            service_id: Click service ID
            secret_key: Click secret key
            test_mode: Use test mode
        """
        self.merchant_id = merchant_id or settings.click_merchant_id
        self.service_id = service_id or settings.click_service_id
        self.secret_key = secret_key or settings.click_secret_key
        self.test_mode = test_mode if test_mode is not None else settings.click_test_mode
        
        self.base_url = "https://my.click.uz/services/pay"
    
    def generate_payment_url(
        self,
        order_id: str,
        amount: Decimal,
        return_url: Optional[str] = None,
    ) -> str:
        """
        Generate Click payment URL.
        
        Args:
            order_id: Order ID
            amount: Amount in UZS
            return_url: URL to return after payment
        
        Returns:
            Payment URL
        """
        transaction_id = str(uuid.uuid4())
        
        url = (
            f"{self.base_url}"
            f"?service_id={self.service_id}"
            f"&merchant_id={self.merchant_id}"
            f"&amount={int(amount)}"
            f"&transaction_param={order_id}"
        )
        
        if return_url:
            url += f"&return_url={return_url}"
        
        return url
    
    def generate_signature(
        self,
        click_trans_id: str,
        service_id: str,
        merchant_trans_id: str,
        amount: str,
        action: str,
        sign_time: str,
    ) -> str:
        """
        Generate Click signature for callback verification.
        
        Args:
            click_trans_id: Click transaction ID
            service_id: Service ID
            merchant_trans_id: Merchant transaction ID
            amount: Amount
            action: Action type
            sign_time: Signature time
        
        Returns:
            MD5 signature
        """
        sign_string = (
            f"{click_trans_id}"
            f"{service_id}"
            f"{self.secret_key}"
            f"{merchant_trans_id}"
            f"{amount}"
            f"{action}"
            f"{sign_time}"
        )
        
        return hashlib.md5(sign_string.encode()).hexdigest()
    
    def verify_callback(
        self,
        data: dict,
    ) -> bool:
        """
        Verify Click callback signature.
        
        Args:
            data: Callback data from Click
        
        Returns:
            True if valid
        """
        expected_sign = self.generate_signature(
            click_trans_id=data.get("click_trans_id", ""),
            service_id=data.get("service_id", ""),
            merchant_trans_id=data.get("merchant_trans_id", ""),
            amount=data.get("amount", ""),
            action=data.get("action", ""),
            sign_time=data.get("sign_time", ""),
        )
        
        return expected_sign == data.get("sign_string", "")
