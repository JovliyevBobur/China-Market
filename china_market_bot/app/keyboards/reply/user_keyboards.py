"""
👤 User Keyboards Module

Reply keyboards for user flows.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_phone_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get phone request keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = {
        "uz": "📱 Telefon raqamni yuborish",
        "ru": "📱 Отправить номер телефона",
        "en": "📱 Send phone number",
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text=texts.get(language, texts["uz"]),
            request_contact=True,
        )
    )
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_location_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get location request keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = {
        "uz": ("📍 Joylashuvni yuborish", "✏️ Qo'lda kiritish"),
        "ru": ("📍 Отправить местоположение", "✏️ Ввести вручную"),
        "en": ("📍 Send location", "✏️ Enter manually"),
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text=texts.get(language, texts["uz"])[0],
            request_location=True,
        )
    )
    builder.row(
        KeyboardButton(text=texts.get(language, texts["uz"])[1])
    )
    
    return builder.as_markup(resize_keyboard=True)


def get_cancel_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get cancel keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = {
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена",
        "en": "❌ Cancel",
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=texts.get(language, texts["uz"])))
    
    return builder.as_markup(resize_keyboard=True)


def get_skip_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get skip keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = {
        "uz": ("⏭️ O'tkazib yuborish", "❌ Bekor qilish"),
        "ru": ("⏭️ Пропустить", "❌ Отмена"),
        "en": ("⏭️ Skip", "❌ Cancel"),
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=texts.get(language, texts["uz"])[0]))
    builder.row(KeyboardButton(text=texts.get(language, texts["uz"])[1]))
    
    return builder.as_markup(resize_keyboard=True)


def get_confirm_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get confirm/cancel keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = {
        "uz": ("✅ Tasdiqlash", "❌ Bekor qilish"),
        "ru": ("✅ Подтвердить", "❌ Отмена"),
        "en": ("✅ Confirm", "❌ Cancel"),
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=texts.get(language, texts["uz"])[0]),
        KeyboardButton(text=texts.get(language, texts["uz"])[1]),
    )
    
    return builder.as_markup(resize_keyboard=True)


def get_language_keyboard() -> ReplyKeyboardMarkup:
    """
    Get language selection keyboard.
    
    Returns:
        ReplyKeyboardMarkup
    """
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="🇺🇿 O'zbek"),
        KeyboardButton(text="🇷🇺 Русский"),
    )
    builder.row(
        KeyboardButton(text="🇬🇧 English"),
    )
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_back_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get back button keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = {
        "uz": "⬅️ Orqaga",
        "ru": "⬅️ Назад",
        "en": "⬅️ Back",
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=texts.get(language, texts["uz"])))
    
    return builder.as_markup(resize_keyboard=True)


def get_yes_no_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """
    Get yes/no keyboard.
    
    Args:
        language: User language code
    
    Returns:
        ReplyKeyboardMarkup
    """
    texts = {
        "uz": ("✅ Ha", "❌ Yo'q"),
        "ru": ("✅ Да", "❌ Нет"),
        "en": ("✅ Yes", "❌ No"),
    }
    
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=texts.get(language, texts["uz"])[0]),
        KeyboardButton(text=texts.get(language, texts["uz"])[1]),
    )
    
    return builder.as_markup(resize_keyboard=True)
