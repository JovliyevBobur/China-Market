"""
🚀 Start Handler Module

Handles /start command and welcome message.
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.config.constants import BOT_NAME, WELCOME_TEXT, Language
from app.keyboards.reply import get_main_menu_keyboard, get_language_keyboard
from app.states import RegistrationStates

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    state: FSMContext,
    user=None,
    is_new_user: bool = False,
):
    """
    Handle /start command.
    
    Args:
        message: Telegram message
        state: FSM state
        user: User model from middleware
        is_new_user: Whether user is newly created
    """
    await state.clear()
    
    # Check if new user needs registration
    if is_new_user:
        await message.answer(
            f"👋 <b>{BOT_NAME}</b> ga xush kelibsiz!\n\n"
            "Iltimos, tilni tanlang:",
            reply_markup=get_language_keyboard(),
            parse_mode="HTML",
        )
        await state.set_state(RegistrationStates.selecting_language)
        return
    
    # Get user language
    language = user.language if user else Language.UZ.value
    
    # Show welcome message and main menu
    welcome = WELCOME_TEXT.format(bot_name=BOT_NAME)
    
    await message.answer(
        welcome,
        reply_markup=get_main_menu_keyboard(language),
        parse_mode="HTML",
    )


@router.message(RegistrationStates.selecting_language, F.text.in_(["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]))
async def process_language(
    message: Message,
    state: FSMContext,
    user=None,
):
    """
    Process language selection.
    
    Args:
        message: Telegram message
        state: FSM state
        user: User model
    """
    language_map = {
        "🇺🇿 O'zbek": "uz",
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en",
    }
    
    language = language_map.get(message.text, "uz")
    
    # Update user language
    if user:
        user.language = language
    
    # Save to state
    await state.update_data(language=language)
    
    # Welcome messages by language
    welcome_texts = {
        "uz": "Ajoyib! Endi telefon raqamingizni yuboring:",
        "ru": "Отлично! Теперь отправьте ваш номер телефона:",
        "en": "Great! Now send your phone number:",
    }
    
    from app.keyboards.reply import get_phone_keyboard
    
    await message.answer(
        welcome_texts[language],
        reply_markup=get_phone_keyboard(language),
    )
    
    await state.set_state(RegistrationStates.entering_phone)


@router.message(RegistrationStates.entering_phone, F.contact)
async def process_phone(
    message: Message,
    state: FSMContext,
    user=None,
):
    """
    Process phone number from contact.
    
    Args:
        message: Telegram message
        state: FSM state
        user: User model
    """
    phone = message.contact.phone_number
    
    # Format phone number
    if not phone.startswith("+"):
        phone = f"+{phone}"
    
    # Update user
    if user:
        user.phone = phone
        user.is_verified = True
    
    # Get language from state
    data = await state.get_data()
    language = data.get("language", "uz")
    
    # Success messages
    success_texts = {
        "uz": "✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\nEndi xarid qilishingiz mumkin.",
        "ru": "✅ Регистрация успешно завершена!\n\nТеперь вы можете делать покупки.",
        "en": "✅ Registration completed successfully!\n\nNow you can start shopping.",
    }
    
    await message.answer(
        success_texts[language],
        reply_markup=get_main_menu_keyboard(language),
    )
    
    await state.clear()


@router.message(RegistrationStates.entering_phone)
async def invalid_phone(message: Message, state: FSMContext):
    """
    Handle invalid phone input.
    
    Args:
        message: Telegram message
        state: FSM state
    """
    data = await state.get_data()
    language = data.get("language", "uz")
    
    error_texts = {
        "uz": "❌ Iltimos, telefon raqamingizni tugma orqali yuboring!",
        "ru": "❌ Пожалуйста, отправьте номер через кнопку!",
        "en": "❌ Please send your phone number using the button!",
    }
    
    from app.keyboards.reply import get_phone_keyboard
    
    await message.answer(
        error_texts[language],
        reply_markup=get_phone_keyboard(language),
    )
