"""
🗄️ Database Middleware Module

Middleware for injecting database session into handlers.
"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database import async_session_factory


class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware that provides database session to handlers.
    
    Adds 'session' to handler data, automatically managing
    session lifecycle (commit on success, rollback on error).
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Process event and inject database session.
        
        Args:
            handler: Next handler in chain
            event: Telegram event
            data: Handler data dict
        
        Returns:
            Handler result
        """
        async with async_session_factory() as session:
            data["session"] = session
            
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
