"""
👑 Admin Filter Module

Filter for admin-only handlers.
"""

from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from app.config import settings
from app.config.constants import UserRole


class AdminFilter(BaseFilter):
    """
    Filter that checks if user is admin.
    
    Checks both settings.admin_ids and database role.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
        user=None,
    ) -> bool:
        """
        Check if user is admin.
        
        Args:
            event: Message or CallbackQuery
            user: User model from middleware (optional)
        
        Returns:
            True if user is admin
        """
        # Get user ID from event
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return False
        
        # Check if in settings.admin_ids
        if user_id in settings.admin_ids:
            return True
        
        # Check database role if user model available
        if user and hasattr(user, "role"):
            return user.role in (
                UserRole.ADMIN,
                UserRole.SUPERADMIN,
                UserRole.MODERATOR,
            )
        
        return False


class IsSuperAdmin(BaseFilter):
    """
    Filter that checks if user is super admin.
    
    Only checks settings.admin_ids (first admin is super).
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
        user=None,
    ) -> bool:
        """
        Check if user is super admin.
        
        Args:
            event: Message or CallbackQuery
            user: User model from middleware (optional)
        
        Returns:
            True if user is super admin
        """
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return False
        
        # First admin in list is super admin
        if settings.admin_ids and user_id == settings.admin_ids[0]:
            return True
        
        # Check database role
        if user and hasattr(user, "role"):
            return user.role == UserRole.SUPERADMIN
        
        return False


class IsModeratorFilter(BaseFilter):
    """
    Filter for moderators (includes admins).
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
        user=None,
    ) -> bool:
        """
        Check if user is moderator.
        
        Args:
            event: Message or CallbackQuery
            user: User model from middleware (optional)
        
        Returns:
            True if user is moderator or higher
        """
        # Admins are also moderators
        admin_filter = AdminFilter()
        if await admin_filter(event, user):
            return True
        
        # Check database role
        if user and hasattr(user, "role"):
            return user.role == UserRole.MODERATOR
        
        return False


# Convenient instances
IsAdmin = AdminFilter()
IsModerator = IsModeratorFilter()
