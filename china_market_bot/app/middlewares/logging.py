"""
📝 Logging Middleware Module

Request logging middleware.
"""

import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware for logging all requests.
    
    Logs user info, event type, and processing time.
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Log event and process.
        
        Args:
            handler: Next handler in chain
            event: Telegram event
            data: Handler data dict
        
        Returns:
            Handler result
        """
        start_time = time.time()
        
        # Get event info for logging
        event_user = data.get("event_from_user")
        user_id = event_user.id if event_user else "unknown"
        username = event_user.username if event_user else "unknown"
        
        # Determine event type and content
        event_type = type(event).__name__
        event_info = self._get_event_info(event)
        
        # Log incoming event
        logger.info(
            f"[{event_type}] User: {user_id} (@{username}) - {event_info}"
        )
        
        try:
            result = await handler(event, data)
            
            # Log success with processing time
            elapsed = (time.time() - start_time) * 1000
            logger.debug(f"[{event_type}] Completed in {elapsed:.2f}ms")
            
            return result
            
        except Exception as e:
            # Log error
            elapsed = (time.time() - start_time) * 1000
            logger.error(
                f"[{event_type}] Error after {elapsed:.2f}ms: {type(e).__name__}: {str(e)}"
            )
            raise
    
    @staticmethod
    def _get_event_info(event: TelegramObject) -> str:
        """
        Get human-readable event info.
        
        Args:
            event: Telegram event
        
        Returns:
            Event info string
        """
        if isinstance(event, Message):
            if event.text:
                # Truncate long texts
                text = event.text[:50] + "..." if len(event.text) > 50 else event.text
                return f"Text: '{text}'"
            elif event.photo:
                return "Photo"
            elif event.video:
                return "Video"
            elif event.document:
                return f"Document: {event.document.file_name}"
            elif event.contact:
                return f"Contact: {event.contact.phone_number}"
            elif event.location:
                return f"Location: {event.location.latitude}, {event.location.longitude}"
            else:
                return "Other content"
        
        elif isinstance(event, CallbackQuery):
            data = event.data or "no data"
            data = data[:30] + "..." if len(data) > 30 else data
            return f"Callback: {data}"
        
        return "Event"
