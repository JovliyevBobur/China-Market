"""
💬 Chat Type Filter Module

Filter for chat type restrictions.
"""

from typing import Union, List

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatType


class ChatTypeFilter(BaseFilter):
    """
    Filter by chat type.
    
    Allows specifying which chat types are allowed.
    """
    
    def __init__(self, chat_types: Union[ChatType, List[ChatType]]):
        """
        Initialize chat type filter.
        
        Args:
            chat_types: Allowed chat type(s)
        """
        if isinstance(chat_types, ChatType):
            self.chat_types = [chat_types]
        else:
            self.chat_types = chat_types
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
    ) -> bool:
        """
        Check if chat type matches.
        
        Args:
            event: Message or CallbackQuery
        
        Returns:
            True if chat type is allowed
        """
        if isinstance(event, Message):
            chat_type = event.chat.type
        elif isinstance(event, CallbackQuery):
            if event.message:
                chat_type = event.message.chat.type
            else:
                return False
        else:
            return False
        
        return chat_type in self.chat_types


class IsPrivateFilter(BaseFilter):
    """
    Filter for private chats only.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
    ) -> bool:
        """
        Check if event is from private chat.
        
        Args:
            event: Message or CallbackQuery
        
        Returns:
            True if private chat
        """
        if isinstance(event, Message):
            return event.chat.type == ChatType.PRIVATE
        elif isinstance(event, CallbackQuery):
            if event.message:
                return event.message.chat.type == ChatType.PRIVATE
        return False


class IsGroupFilter(BaseFilter):
    """
    Filter for group chats only.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
    ) -> bool:
        """
        Check if event is from group chat.
        
        Args:
            event: Message or CallbackQuery
        
        Returns:
            True if group or supergroup
        """
        if isinstance(event, Message):
            return event.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
        elif isinstance(event, CallbackQuery):
            if event.message:
                return event.message.chat.type in (
                    ChatType.GROUP,
                    ChatType.SUPERGROUP,
                )
        return False


class IsChannelFilter(BaseFilter):
    """
    Filter for channel posts only.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
    ) -> bool:
        """
        Check if event is from channel.
        
        Args:
            event: Message or CallbackQuery
        
        Returns:
            True if channel
        """
        if isinstance(event, Message):
            return event.chat.type == ChatType.CHANNEL
        elif isinstance(event, CallbackQuery):
            if event.message:
                return event.message.chat.type == ChatType.CHANNEL
        return False


# Convenient instances
IsPrivate = IsPrivateFilter()
IsGroup = IsGroupFilter()
IsChannel = IsChannelFilter()
PrivateOnly = ChatTypeFilter(ChatType.PRIVATE)
GroupOnly = ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP])
