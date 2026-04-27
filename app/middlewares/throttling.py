"""
⏱️ Throttling Middleware Module

Rate limiting middleware to prevent spam.
"""

import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from app.config import settings


class ThrottlingMiddleware(BaseMiddleware):
    """
    Rate limiting middleware to prevent spam.
    
    Tracks user request rates and temporarily bans
    users who exceed the limit.
    """
    
    def __init__(
        self,
        rate_limit: float = 0.5,
        max_requests: int = 30,
        ban_time: int = 300,
    ):
        """
        Initialize throttling middleware.
        
        Args:
            rate_limit: Minimum seconds between requests
            max_requests: Max requests before ban
            ban_time: Ban duration in seconds
        """
        self.rate_limit = rate_limit
        self.max_requests = max_requests
        self.ban_time = ban_time
        
        # User tracking data
        self.users_data: Dict[int, Dict] = defaultdict(
            lambda: {
                "last_request": 0,
                "request_count": 0,
                "banned_until": 0,
                "warned": False,
            }
        )
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        """
        Process event with rate limiting.
        
        Args:
            handler: Next handler in chain
            event: Telegram event
            data: Handler data dict
        
        Returns:
            Handler result or None if throttled
        """
        # Get user from event
        event_user = data.get("event_from_user")
        
        if not event_user:
            return await handler(event, data)
        
        user_id = event_user.id
        current_time = time.time()
        user_data = self.users_data[user_id]
        
        # Check if user is banned
        if current_time < user_data["banned_until"]:
            remaining = int(user_data["banned_until"] - current_time)
            
            # Send warning only once per ban
            if isinstance(event, Message) and not user_data.get("ban_notified"):
                await event.answer(
                    f"⏳ Juda ko'p so'rov yubordingiz.\n"
                    f"Iltimos, {remaining} soniya kutib turing.",
                )
                user_data["ban_notified"] = True
            
            return None
        
        # Reset ban notification flag
        user_data["ban_notified"] = False
        
        # Check rate limit
        time_since_last = current_time - user_data["last_request"]
        
        if time_since_last < self.rate_limit:
            user_data["request_count"] += 1
            
            # Check if should ban
            if user_data["request_count"] >= self.max_requests:
                user_data["banned_until"] = current_time + self.ban_time
                user_data["request_count"] = 0
                
                if isinstance(event, Message):
                    await event.answer(
                        f"🚫 Juda ko'p so'rov!\n"
                        f"Siz {self.ban_time // 60} daqiqaga bloklangansiz.",
                    )
                
                return None
            
            # Warn user
            if not user_data["warned"] and user_data["request_count"] > self.max_requests // 2:
                user_data["warned"] = True
                if isinstance(event, Message):
                    await event.answer(
                        "⚠️ Iltimos, sekinroq so'rov yuboring!",
                    )
        else:
            # Reset counter if enough time passed
            user_data["request_count"] = 0
            user_data["warned"] = False
        
        user_data["last_request"] = current_time
        
        return await handler(event, data)
    
    def reset_user(self, user_id: int) -> None:
        """
        Reset user throttling data.
        
        Args:
            user_id: Telegram user ID
        """
        if user_id in self.users_data:
            del self.users_data[user_id]
    
    def ban_user(self, user_id: int, duration: int) -> None:
        """
        Manually ban user.
        
        Args:
            user_id: Telegram user ID
            duration: Ban duration in seconds
        """
        self.users_data[user_id]["banned_until"] = time.time() + duration
