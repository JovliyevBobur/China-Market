"""
❌ Cancel Handler Module

Handles cancel command and back navigation.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.callbacks import CancelCallback, BackCallback
from app.keyboards.reply import get_main_menu_keyboard

router = Router(name="cancel")


@router.message(Command("cancel"))
@router.message(F.text.in_(["❌ Bekor qilish", "❌ Отмена", "❌ Cancel"]))
async def cmd_cancel(
    message: Message,
    state: FSMContext,
    user=None,
):
    """
    Handle cancel command.
    
    Args:
        message: Telegram message
        state: FSM state
        user: User model
    """
    await state.clear()
    
    language = user.language if user else "uz"
    
    texts = {
        "uz": "❌ Amal bekor qilindi.\n\nAsosiy menyu:",
        "ru": "❌ Действие отменено.\n\nГлавное меню:",
        "en": "❌ Action cancelled.\n\nMain menu:",
    }
    
    await message.answer(
        texts.get(language, texts["uz"]),
        reply_markup=get_main_menu_keyboard(language),
    )


@router.callback_query(CancelCallback.filter())
async def callback_cancel(
    callback: CallbackQuery,
    callback_data: CancelCallback,
    state: FSMContext,
    user=None,
):
    """
    Handle cancel callback.
    
    Args:
        callback: Callback query
        callback_data: Cancel callback data
        state: FSM state
        user: User model
    """
    await state.clear()
    
    await callback.message.edit_text("❌ Bekor qilindi.")
    await callback.answer()


@router.callback_query(BackCallback.filter(F.to == "main"))
async def back_to_main(
    callback: CallbackQuery,
    state: FSMContext,
    user=None,
):
    """
    Handle back to main menu.
    
    Args:
        callback: Callback query
        state: FSM state
        user: User model
    """
    await state.clear()
    
    language = user.language if user else "uz"
    
    await callback.message.delete()
    await callback.message.answer(
        "🏠 Asosiy menyu:",
        reply_markup=get_main_menu_keyboard(language),
    )
    
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    """Handle no-operation callbacks (for display-only buttons)."""
    await callback.answer()
