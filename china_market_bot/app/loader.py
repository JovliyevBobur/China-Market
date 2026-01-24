"""
🤖 Bot Loader Module

Bot, Dispatcher, and other global objects initialization.
"""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio import Redis

from app.config import settings


def create_bot() -> Bot:
    """
    Create and configure bot instance.
    
    Returns:
        Bot: Configured bot instance
    """
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )


def create_storage() -> RedisStorage | MemoryStorage:
    """
    Create FSM storage.
    
    Uses Redis if available, falls back to memory storage.
    
    Returns:
        Storage instance
    """
    try:
        redis = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            decode_responses=True,
        )
        return RedisStorage(redis=redis)
    except Exception:
        # Fallback to memory storage
        return MemoryStorage()


def create_dispatcher(storage=None) -> Dispatcher:
    """
    Create and configure dispatcher.
    
    Args:
        storage: FSM storage (optional)
    
    Returns:
        Dispatcher: Configured dispatcher instance
    """
    if storage is None:
        storage = create_storage()
    
    dp = Dispatcher(storage=storage)
    
    return dp


# Global instances
bot = create_bot()
storage = create_storage()
dp = create_dispatcher(storage)
