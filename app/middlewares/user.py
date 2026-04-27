"""
👤 User Middleware Module

Middleware for user registration and injection.
"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import UserRepository


class UserMiddleware(BaseMiddleware):
    """
    Middleware that ensures user exists and injects user model.
    
    Creates user if not exists, updates user info if changed.
    Adds 'user' (database model) to handler data.
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Process event and inject user model.
        
        Args:
            handler: Next handler in chain
            event: Telegram event
            data: Handler data dict
        
        Returns:
            Handler result
        """
        # Get Telegram user from event
        event_user: TelegramUser = data.get("event_from_user")
        
        if not event_user:
            # No user in this event (e.g., channel post)
            return await handler(event, data)
        
        # Get session (must be after DatabaseMiddleware)
        session: AsyncSession = data.get("session")
        
        if not session:
            # No session available
            return await handler(event, data)
        
        # Get or create user
        user_repo = UserRepository(session)
        
        user, created = await user_repo.get_or_create(
            telegram_id=event_user.id,
            username=event_user.username,
            first_name=event_user.first_name,
            last_name=event_user.last_name,
        )
        
        # Check if user is banned
        if user.is_banned:
            # You can handle banned users here
            # For now, we'll pass the user anyway
            pass
        
        # Update last activity
        user.update_activity()
        
        # Inject user into data
        data["user"] = user
        data["user_repo"] = user_repo
        data["is_new_user"] = created
        
        return await handler(event, data)
