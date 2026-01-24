"""
🏪 Seller Filter Module

Filter for seller-only handlers.
"""

from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from app.config.constants import ModerationStatus, UserRole


class SellerFilter(BaseFilter):
    """
    Filter that checks if user is a seller.
    
    Checks if user has seller role and approved profile.
    """
    
    def __init__(self, require_approved: bool = True):
        """
        Initialize seller filter.
        
        Args:
            require_approved: Require seller to be approved
        """
        self.require_approved = require_approved
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
        user=None,
    ) -> bool:
        """
        Check if user is seller.
        
        Args:
            event: Message or CallbackQuery
            user: User model from middleware (optional)
        
        Returns:
            True if user is seller
        """
        if not user:
            return False
        
        # Check role
        if not hasattr(user, "role"):
            return False
        
        # Admins can access seller features
        if user.role in (UserRole.ADMIN, UserRole.SUPERADMIN):
            return True
        
        # Check if seller
        if user.role != UserRole.SELLER:
            return False
        
        # Check approved status if required
        if self.require_approved:
            if not hasattr(user, "seller_profile") or not user.seller_profile:
                return False
            
            seller = user.seller_profile
            
            if seller.moderation_status != ModerationStatus.APPROVED:
                return False
            
            if not seller.is_active:
                return False
        
        return True


class HasSellerProfileFilter(BaseFilter):
    """
    Filter that checks if user has seller profile.
    
    Doesn't require approval, just existence.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
        user=None,
    ) -> bool:
        """
        Check if user has seller profile.
        
        Args:
            event: Message or CallbackQuery
            user: User model from middleware (optional)
        
        Returns:
            True if user has seller profile
        """
        if not user:
            return False
        
        return (
            hasattr(user, "seller_profile")
            and user.seller_profile is not None
        )


class SellerPendingFilter(BaseFilter):
    """
    Filter for sellers with pending approval.
    """
    
    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
        user=None,
    ) -> bool:
        """
        Check if user is seller with pending status.
        
        Args:
            event: Message or CallbackQuery
            user: User model from middleware (optional)
        
        Returns:
            True if seller pending
        """
        if not user:
            return False
        
        if not hasattr(user, "seller_profile") or not user.seller_profile:
            return False
        
        return user.seller_profile.moderation_status == ModerationStatus.PENDING


# Convenient instances
IsSeller = SellerFilter()
IsApprovedSeller = SellerFilter(require_approved=True)
IsPendingSeller = SellerPendingFilter()
HasSellerProfile = HasSellerProfileFilter()
