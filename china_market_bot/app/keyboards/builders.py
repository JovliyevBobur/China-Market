"""
🛠️ Keyboard Builders Module

Utility classes for building keyboards.
"""

from typing import List, Optional, Union

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class KeyboardBuilder:
    """
    Utility class for building keyboards.
    """
    
    @staticmethod
    def inline(
        buttons: List[List[Union[InlineKeyboardButton, dict]]],
    ) -> InlineKeyboardMarkup:
        """
        Build inline keyboard from button list.
        
        Args:
            buttons: 2D list of buttons or button dicts
        
        Returns:
            InlineKeyboardMarkup
        """
        builder = InlineKeyboardBuilder()
        
        for row in buttons:
            row_buttons = []
            for button in row:
                if isinstance(button, dict):
                    row_buttons.append(InlineKeyboardButton(**button))
                else:
                    row_buttons.append(button)
            builder.row(*row_buttons)
        
        return builder.as_markup()
    
    @staticmethod
    def reply(
        buttons: List[List[Union[KeyboardButton, str]]],
        resize: bool = True,
        one_time: bool = False,
        placeholder: Optional[str] = None,
    ) -> ReplyKeyboardMarkup:
        """
        Build reply keyboard from button list.
        
        Args:
            buttons: 2D list of buttons or text strings
            resize: Resize keyboard to fit
            one_time: Hide after use
            placeholder: Input placeholder text
        
        Returns:
            ReplyKeyboardMarkup
        """
        builder = ReplyKeyboardBuilder()
        
        for row in buttons:
            row_buttons = []
            for button in row:
                if isinstance(button, str):
                    row_buttons.append(KeyboardButton(text=button))
                else:
                    row_buttons.append(button)
            builder.row(*row_buttons)
        
        return builder.as_markup(
            resize_keyboard=resize,
            one_time_keyboard=one_time,
            input_field_placeholder=placeholder,
        )
    
    @staticmethod
    def remove() -> ReplyKeyboardRemove:
        """
        Get keyboard remove markup.
        
        Returns:
            ReplyKeyboardRemove
        """
        return ReplyKeyboardRemove()
    
    @staticmethod
    def url_button(text: str, url: str) -> InlineKeyboardButton:
        """
        Create URL button.
        
        Args:
            text: Button text
            url: URL to open
        
        Returns:
            InlineKeyboardButton
        """
        return InlineKeyboardButton(text=text, url=url)
    
    @staticmethod
    def callback_button(text: str, callback_data: str) -> InlineKeyboardButton:
        """
        Create callback button.
        
        Args:
            text: Button text
            callback_data: Callback data string
        
        Returns:
            InlineKeyboardButton
        """
        return InlineKeyboardButton(text=text, callback_data=callback_data)
    
    @staticmethod
    def phone_button(text: str = "📱 Telefon raqamni yuborish") -> KeyboardButton:
        """
        Create phone request button.
        
        Args:
            text: Button text
        
        Returns:
            KeyboardButton
        """
        return KeyboardButton(text=text, request_contact=True)
    
    @staticmethod
    def location_button(text: str = "📍 Joylashuvni yuborish") -> KeyboardButton:
        """
        Create location request button.
        
        Args:
            text: Button text
        
        Returns:
            KeyboardButton
        """
        return KeyboardButton(text=text, request_location=True)
    
    @staticmethod
    def webapp_button(text: str, url: str) -> InlineKeyboardButton:
        """
        Create web app button.
        
        Args:
            text: Button text
            url: Web app URL
        
        Returns:
            InlineKeyboardButton
        """
        from aiogram.types import WebAppInfo
        
        return InlineKeyboardButton(
            text=text,
            web_app=WebAppInfo(url=url),
        )
    
    @staticmethod
    def back_button(
        text: str = "⬅️ Orqaga",
        callback_data: str = "back",
    ) -> InlineKeyboardButton:
        """
        Create standard back button.
        
        Args:
            text: Button text
            callback_data: Callback data
        
        Returns:
            InlineKeyboardButton
        """
        return InlineKeyboardButton(text=text, callback_data=callback_data)
    
    @staticmethod
    def cancel_button(
        text: str = "❌ Bekor qilish",
        callback_data: str = "cancel",
    ) -> InlineKeyboardButton:
        """
        Create standard cancel button.
        
        Args:
            text: Button text
            callback_data: Callback data
        
        Returns:
            InlineKeyboardButton
        """
        return InlineKeyboardButton(text=text, callback_data=callback_data)


def create_inline_keyboard(
    buttons: list[tuple[str, str]],
    row_width: int = 2,
) -> InlineKeyboardMarkup:
    """
    Create inline keyboard from tuples.
    
    Args:
        buttons: List of (text, callback_data) tuples
        row_width: Buttons per row
    
    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)
    
    builder.adjust(row_width)
    
    return builder.as_markup()


def create_reply_keyboard(
    buttons: list[str],
    row_width: int = 2,
    resize: bool = True,
) -> ReplyKeyboardMarkup:
    """
    Create reply keyboard from strings.
    
    Args:
        buttons: List of button texts
        row_width: Buttons per row
        resize: Resize keyboard
    
    Returns:
        ReplyKeyboardMarkup
    """
    builder = ReplyKeyboardBuilder()
    
    for text in buttons:
        builder.button(text=text)
    
    builder.adjust(row_width)
    
    return builder.as_markup(resize_keyboard=resize)
