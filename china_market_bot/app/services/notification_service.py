"""
📊 Notification Service Module

Service for sending notifications to users.
"""

import asyncio
from typing import List, Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from loguru import logger

from app.config.constants import OrderStatus, ORDER_STATUS_EMOJI


class NotificationService:
    """
    Service for sending notifications to users.
    """
    
    def __init__(self, bot: Bot):
        """
        Initialize notification service.
        
        Args:
            bot: Bot instance
        """
        self.bot = bot
    
    async def notify_order_status(
        self,
        user_id: int,
        order_id: int,
        order_number: str,
        status: OrderStatus,
        details: str = "",
    ) -> bool:
        """
        Notify user about order status change.
        
        Args:
            user_id: User Telegram ID
            order_id: Order ID
            order_number: Order number
            status: New order status
            details: Additional details
        
        Returns:
            True if sent successfully
        """
        emoji = ORDER_STATUS_EMOJI.get(status, "📋")
        
        status_texts = {
            OrderStatus.PENDING: "Kutilmoqda",
            OrderStatus.CONFIRMED: "Tasdiqlandi",
            OrderStatus.PROCESSING: "Tayyorlanmoqda",
            OrderStatus.SHIPPED: "Yuborildi",
            OrderStatus.DELIVERED: "Yetkazildi",
            OrderStatus.COMPLETED: "Tugallandi",
            OrderStatus.CANCELLED: "Bekor qilindi",
            OrderStatus.REFUNDED: "Qaytarildi",
        }
        
        status_text = status_texts.get(status, str(status.value))
        
        message = (
            f"{emoji} <b>Buyurtma #{order_number}</b>\n\n"
            f"Holat: <b>{status_text}</b>"
        )
        
        if details:
            message += f"\n\n{details}"
        
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode="HTML",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to notify user {user_id}: {e}")
            return False
    
    async def notify_seller_new_order(
        self,
        seller_telegram_id: int,
        order_number: str,
        item_count: int,
        total_amount: float,
    ) -> bool:
        """
        Notify seller about new order.
        
        Args:
            seller_telegram_id: Seller Telegram ID
            order_number: Order number
            item_count: Number of items
            total_amount: Total order amount
        
        Returns:
            True if sent successfully
        """
        total = f"{total_amount:,.0f}".replace(",", " ")
        
        message = (
            f"🛒 <b>Yangi buyurtma!</b>\n\n"
            f"Buyurtma: #{order_number}\n"
            f"Mahsulotlar: {item_count}\n"
            f"Jami: {total} so'm\n\n"
            f"Iltimos, buyurtmani qayta ishlang."
        )
        
        try:
            await self.bot.send_message(
                chat_id=seller_telegram_id,
                text=message,
                parse_mode="HTML",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to notify seller {seller_telegram_id}: {e}")
            return False
    
    async def broadcast(
        self,
        user_ids: List[int],
        message: str,
        keyboard: Optional[InlineKeyboardMarkup] = None,
        disable_notification: bool = False,
    ) -> dict:
        """
        Broadcast message to multiple users.
        
        Args:
            user_ids: List of Telegram user IDs
            message: Message text
            keyboard: Optional inline keyboard
            disable_notification: Disable notification sound
        
        Returns:
            Dictionary with success and failed counts
        """
        success = 0
        failed = 0
        blocked = 0
        
        for user_id in user_ids:
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode="HTML",
                    reply_markup=keyboard,
                    disable_notification=disable_notification,
                )
                success += 1
                
                # Rate limiting - 30 messages per second max
                await asyncio.sleep(0.05)
                
            except Exception as e:
                error_str = str(e).lower()
                
                if "blocked" in error_str or "deactivated" in error_str:
                    blocked += 1
                else:
                    failed += 1
                    logger.debug(f"Failed to send broadcast to {user_id}: {e}")
        
        return {
            "success": success,
            "failed": failed,
            "blocked": blocked,
            "total": len(user_ids),
        }
    
    async def send_admin_alert(
        self,
        admin_ids: List[int],
        title: str,
        message: str,
        is_urgent: bool = False,
    ) -> None:
        """
        Send alert to admins.
        
        Args:
            admin_ids: List of admin Telegram IDs
            title: Alert title
            message: Alert message
            is_urgent: Is this urgent
        """
        emoji = "🚨" if is_urgent else "ℹ️"
        
        text = f"{emoji} <b>{title}</b>\n\n{message}"
        
        for admin_id in admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.error(f"Failed to send admin alert to {admin_id}: {e}")
    
    async def send_welcome_message(
        self,
        user_id: int,
        first_name: str,
        keyboard: Optional[InlineKeyboardMarkup] = None,
    ) -> bool:
        """
        Send welcome message to new user.
        
        Args:
            user_id: User Telegram ID
            first_name: User's first name
            keyboard: Optional inline keyboard
        
        Returns:
            True if sent successfully
        """
        message = (
            f"👋 Salom, <b>{first_name}</b>!\n\n"
            f"🛒 <b>China Market</b> ga xush kelibsiz!\n\n"
            f"Bu yerda siz:\n"
            f"• 📦 Mahsulotlarni ko'rishingiz\n"
            f"• 🔍 Qidiruv qilishingiz\n"
            f"• 🛒 Savatingizga qo'shishingiz\n"
            f"• 💳 Xarid qilishingiz mumkin!\n\n"
            f"Yaxshi xaridlar! 🎉"
        )
        
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome to {user_id}: {e}")
            return False
