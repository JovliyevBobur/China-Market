"""
🚨 Error Handler Module

Global error handling for handlers.
"""

from aiogram import Router
from aiogram.types import ErrorEvent
from loguru import logger

router = Router(name="errors")


@router.errors()
async def error_handler(event: ErrorEvent):
    """
    Handle all errors in handlers.
    
    Args:
        event: Error event containing exception and update
    """
    logger.exception(
        f"Error processing update: {event.exception}",
        exc_info=event.exception,
    )
    
    # Try to notify user
    update = event.update
    
    if update.message:
        try:
            await update.message.answer(
                "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
            )
        except Exception:
            pass
    
    elif update.callback_query:
        try:
            await update.callback_query.answer(
                "❌ Xatolik yuz berdi!",
                show_alert=True,
            )
        except Exception:
            pass
