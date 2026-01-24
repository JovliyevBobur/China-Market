"""
🚀 Main Application Entry Point

Bot startup and shutdown logic.
"""

import asyncio
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from loguru import logger

from app.config import settings
from app.database import session_manager
from app.handlers import main_router
from app.loader import bot, dp
from app.middlewares import (
    DatabaseMiddleware,
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    ThrottlingMiddleware,
    UserMiddleware,
)


def setup_logging() -> None:
    """Configure logging with loguru."""
    # Remove default handler
    logger.remove()
    
    # Console output
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # File output
    log_path = Path(settings.log_path)
    log_path.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_path / "bot_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="00:00",
        retention="30 days",
        compression="zip",
    )


def setup_middlewares(dp: Dispatcher) -> None:
    """
    Register all middlewares.
    
    Args:
        dp: Dispatcher instance
    """
    # Order matters! First registered = first executed (outer)
    
    # Error handling (outermost)
    dp.message.middleware(ErrorHandlingMiddleware())
    dp.callback_query.middleware(ErrorHandlingMiddleware())
    
    # Logging
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    
    # Throttling
    dp.message.middleware(ThrottlingMiddleware(
        rate_limit=0.5,
        max_requests=settings.rate_limit_requests,
        ban_time=settings.ban_time_seconds,
    ))
    
    # Database session
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    
    # User registration (must be after database)
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    
    logger.info("Middlewares registered")


def setup_routers(dp: Dispatcher) -> None:
    """
    Register all routers.
    
    Args:
        dp: Dispatcher instance
    """
    dp.include_router(main_router)
    logger.info("Routers registered")


async def on_startup(bot: Bot) -> None:
    """
    Actions on bot startup.
    
    Args:
        bot: Bot instance
    """
    logger.info("Bot starting up...")
    
    # Get bot info
    bot_info = await bot.get_me()
    logger.info(f"Bot: @{bot_info.username} (ID: {bot_info.id})")
    
    # Notify admins
    for admin_id in settings.admin_ids[:3]:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="🤖 Bot ishga tushdi!",
            )
        except Exception as e:
            logger.warning(f"Failed to notify admin {admin_id}: {e}")
    
    logger.info("Bot started successfully!")


async def on_shutdown(bot: Bot) -> None:
    """
    Actions on bot shutdown.
    
    Args:
        bot: Bot instance
    """
    logger.info("Bot shutting down...")
    
    # Close database connections
    await session_manager.close()
    
    # Notify admins
    for admin_id in settings.admin_ids[:3]:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="🔴 Bot to'xtatildi.",
            )
        except Exception:
            pass
    
    # Close bot session
    await bot.session.close()
    
    logger.info("Bot stopped.")


async def main() -> None:
    """Main function to run the bot."""
    # Setup logging
    setup_logging()
    
    logger.info("=" * 50)
    logger.info("🛒 China Market Bot")
    logger.info("=" * 50)
    
    # Setup middlewares and routers
    setup_middlewares(dp)
    setup_routers(dp)
    
    # Register startup/shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    try:
        logger.info("Starting polling...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
    finally:
        await on_shutdown(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
