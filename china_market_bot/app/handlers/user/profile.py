"""
👤 Profile Handler Module

User profile management - view, edit, change language.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from app.config import settings
from app.config.constants import Language
from app.database.models import User
from app.keyboards.inline.catalog_kb import create_back_button
from app.keyboards.reply.main_menu import create_main_menu
from app.states.user_states import ProfileStates

router = Router(name="profile")


@router.message(Command("profile"))
@router.message(F.text.in_(["👤 Profil", "👤 Профиль", "👤 Profile"]))
async def show_profile(message: Message, user: User) -> None:
    """Show user profile."""
    
    text = (
        f"👤 <b>Sizning profilingiz</b>\n\n"
        f"🆔 ID: <code>{user.telegram_id}</code>\n"
        f"👤 Ism: {user.full_name}\n"
        f"📱 Telefon: {user.phone or 'Kiritilmagan'}\n"
        f"📧 Email: {user.email or 'Kiritilmagan'}\n"
        f"🌍 Til: {user.language.upper()}\n"
        f"📅 Ro'yxatdan o'tgan: {user.created_at.strftime('%d.%m.%Y')}\n"
        f"✅ Tasdiqlangan: {'Ha' if user.is_verified else 'Yo\\'q'}\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Ismni o'zgartirish", callback_data="profile:edit_name"),
            InlineKeyboardButton(text="📱 Telefon", callback_data="profile:edit_phone"),
        ],
        [
            InlineKeyboardButton(text="🌍 Tilni o'zgartirish", callback_data="profile:change_lang"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main"),
        ],
    ])
    
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "profile:change_lang")
async def change_language(callback: CallbackQuery) -> None:
    """Show language selection."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="profile:back"),
        ],
    ])
    
    await callback.message.edit_text(
        "🌍 <b>Tilni tanlang:</b>",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery, user: User, session) -> None:
    """Set user language."""
    lang = callback.data.split(":")[1]
    
    user.language = lang
    await session.commit()
    
    lang_names = {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}
    
    await callback.message.edit_text(
        f"✅ Til {lang_names.get(lang, lang)} ga o'zgartirildi!",
    )
    await callback.answer()


@router.callback_query(F.data == "profile:edit_name")
async def edit_name_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Start name editing."""
    await state.set_state(ProfileStates.entering_name)
    
    await callback.message.edit_text(
        "✏️ <b>Yangi ismingizni kiriting:</b>\n\n"
        "<i>Bekor qilish uchun /cancel buyrug'ini yuboring</i>",
    )
    await callback.answer()


@router.message(ProfileStates.entering_name)
async def process_name(message: Message, user: User, session, state: FSMContext) -> None:
    """Process new name."""
    name = message.text.strip()
    
    if len(name) < 2 or len(name) > 100:
        await message.answer("❌ Ism 2-100 belgi orasida bo'lishi kerak!")
        return
    
    # Split name
    parts = name.split(" ", 1)
    user.first_name = parts[0]
    user.last_name = parts[1] if len(parts) > 1 else None
    
    await session.commit()
    await state.clear()
    
    await message.answer(
        f"✅ Ismingiz '{name}' ga o'zgartirildi!",
        reply_markup=create_main_menu(),
    )


@router.callback_query(F.data == "profile:edit_phone")
async def edit_phone_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Start phone editing."""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    await state.set_state(ProfileStates.entering_phone)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True,
    )
    
    await callback.message.answer(
        "📱 <b>Telefon raqamingizni yuboring:</b>\n\n"
        "Quyidagi tugmani bosing yoki raqamni qo'lda kiriting (+998XXXXXXXXX)",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(ProfileStates.entering_phone, F.contact)
async def process_phone_contact(message: Message, user: User, session, state: FSMContext) -> None:
    """Process phone from contact."""
    phone = message.contact.phone_number
    
    if not phone.startswith("+"):
        phone = f"+{phone}"
    
    user.phone = phone
    user.is_verified = True
    
    await session.commit()
    await state.clear()
    
    await message.answer(
        f"✅ Telefon raqamingiz {phone} ga saqlandi!",
        reply_markup=create_main_menu(),
    )


@router.message(ProfileStates.entering_phone)
async def process_phone_text(message: Message, user: User, session, state: FSMContext) -> None:
    """Process phone from text."""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=create_main_menu())
        return
    
    import re
    phone = message.text.strip()
    
    # Validate phone
    if not re.match(r'^\+998[0-9]{9}$', phone):
        await message.answer(
            "❌ Noto'g'ri format!\n"
            "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak."
        )
        return
    
    user.phone = phone
    await session.commit()
    await state.clear()
    
    await message.answer(
        f"✅ Telefon raqamingiz {phone} ga saqlandi!",
        reply_markup=create_main_menu(),
    )


@router.callback_query(F.data == "profile:back")
async def back_to_profile(callback: CallbackQuery, user: User) -> None:
    """Go back to profile."""
    # Re-use show_profile logic
    text = (
        f"👤 <b>Sizning profilingiz</b>\n\n"
        f"🆔 ID: <code>{user.telegram_id}</code>\n"
        f"👤 Ism: {user.full_name}\n"
        f"📱 Telefon: {user.phone or 'Kiritilmagan'}\n"
        f"🌍 Til: {user.language.upper()}\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Ismni o'zgartirish", callback_data="profile:edit_name"),
            InlineKeyboardButton(text="📱 Telefon", callback_data="profile:edit_phone"),
        ],
        [
            InlineKeyboardButton(text="🌍 Tilni o'zgartirish", callback_data="profile:change_lang"),
        ],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
