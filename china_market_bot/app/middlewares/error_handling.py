"""
🚨 Error Handling Middleware Module

Global error handling middleware.
"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, Update
from loguru import logger

from app.config.constants import ErrorMessages


class ErrorHandlingMiddleware(BaseMiddleware):
    """
    Global error handling middleware.
    
    Catches all unhandled exceptions and sends
    user-friendly error messages.
    """
    
    def __init__(self, notify_admins: bool = True):
        """
        Initialize error handler.
        
        Args:
            notify_admins: Whether to notify admins on errors
        """
        self.notify_admins = notify_admins
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Handle event with error catching.
        
        Args:
            handler: Next handler in chain
            event: Telegram event
            data: Handler data dict
        
        Returns:
            Handler result
        """
        try:
            return await handler(event, data)
            
        except Exception as e:
            # Log the error
            logger.exception(f"Unhandled error: {type(e).__name__}: {str(e)}")
            
            # Send user-friendly message
            await self._send_error_message(event, data)
            
            # Notify admins if enabled
            if self.notify_admins:
                await self._notify_admins(event, data, e)
            
            # Don't re-raise to prevent bot crash
            return None
    
    async def _send_error_message(
        self,
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> None:
        """
        Send user-friendly error message.
        
        Args:
            event: Telegram event
            data: Handler data dict
        """
        error_text = ErrorMessages.GENERAL_ERROR
        
        try:
            if isinstance(event, Message):
                await event.answer(error_text)
            elif isinstance(event, CallbackQuery):
                await event.answer(error_text, show_alert=True)
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    
    async def _notify_admins(
        self,
        event: TelegramObject,
        data: Dict[str, Any],
        error: Exception,
    ) -> None:
        """
        Notify admins about the error.
        
        Args:
            event: Telegram event
            data: Handler data dict
            error: The exception that occurred
        """
        from app.config import settings
        
        if not settings.admin_ids:
            return
        
        # Get event info
        event_user = data.get("event_from_user")
        user_id = event_user.id if event_user else "unknown"
        username = event_user.username if event_user else "unknown"
        
        # Build error report
        error_report = (
            f"🚨 <b>Error Report</b>\n\n"
            f"<b>Error:</b> <code>{type(error).__name__}</code>\n"
            f"<b>Message:</b> {str(error)[:500]}\n\n"
            f"<b>User:</b> {user_id} (@{username})\n"
            f"<b>Event:</b> {type(event).__name__}"
        )
        
        # Send to admins
        bot = data.get("bot")
        if bot:
            for admin_id in settings.admin_ids[:3]:  # Limit to first 3 admins
                try:
                    await bot.send_message(
                        chat_id=admin_id,
                        text=error_report,
                        parse_mode="HTML",
                    )
                except Exception as e:
                    logger.error(f"Failed to notify admin {admin_id}: {e}")
