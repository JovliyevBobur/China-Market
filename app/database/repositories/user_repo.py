"""
👤 User Repository Module

Repository for user-related database operations.
"""

from typing import Optional, Sequence

from sqlalchemy import func, select

from app.config.constants import UserRole
from app.database.models import User

from .base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository with specialized queries.
    """
    
    model = User
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Get user by Telegram ID.
        
        Args:
            telegram_id: Telegram user ID
        
        Returns:
            User or None
        """
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, phone: str) -> Optional[User]:
        """
        Get user by phone number.
        
        Args:
            phone: Phone number
        
        Returns:
            User or None
        """
        result = await self.session.execute(
            select(User).where(User.phone == phone)
        )
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        language: str = "uz",
    ) -> tuple[User, bool]:
        """
        Get existing user or create new one.
        
        Args:
            telegram_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            last_name: User's last name
            language: Preferred language
        
        Returns:
            Tuple of (User, created: bool)
        """
        user = await self.get_by_telegram_id(telegram_id)
        
        if user:
            # Update user info if changed
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.update_activity()
            await self.session.flush()
            return user, False
        
        # Create new user
        user = await self.create(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language=language,
        )
        return user, True
    
    async def get_admins(self) -> Sequence[User]:
        """
        Get all admin users.
        
        Returns:
            Sequence of admin users
        """
        result = await self.session.execute(
            select(User).where(
                User.role.in_([UserRole.ADMIN, UserRole.SUPERADMIN, UserRole.MODERATOR])
            )
        )
        return result.scalars().all()
    
    async def get_sellers(
        self,
        limit: int = 100,
        offset: int = 0,
        is_active: bool = True,
    ) -> Sequence[User]:
        """
        Get all seller users.
        
        Args:
            limit: Maximum number of records
            offset: Number of records to skip
            is_active: Filter by active status
        
        Returns:
            Sequence of seller users
        """
        stmt = select(User).where(
            User.role == UserRole.SELLER,
            User.is_active == is_active,
        ).limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def search(
        self,
        query: str,
        limit: int = 20,
    ) -> Sequence[User]:
        """
        Search users by username, name, or phone.
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            Sequence of matching users
        """
        search_pattern = f"%{query}%"
        
        stmt = select(User).where(
            (User.username.ilike(search_pattern)) |
            (User.first_name.ilike(search_pattern)) |
            (User.last_name.ilike(search_pattern)) |
            (User.phone.ilike(search_pattern))
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def count_by_role(self, role: UserRole) -> int:
        """
        Count users by role.
        
        Args:
            role: User role
        
        Returns:
            Count of users with given role
        """
        result = await self.session.execute(
            select(func.count()).select_from(User).where(User.role == role)
        )
        return result.scalar_one()
    
    async def count_active(self) -> int:
        """
        Count active users.
        
        Returns:
            Count of active users
        """
        result = await self.session.execute(
            select(func.count()).select_from(User).where(
                User.is_active == True,
                User.is_banned == False,
            )
        )
        return result.scalar_one()
    
    async def ban_user(
        self,
        user_id: int,
        reason: str,
    ) -> Optional[User]:
        """
        Ban user.
        
        Args:
            user_id: User ID
            reason: Ban reason
        
        Returns:
            Updated user or None
        """
        user = await self.get_by_id(user_id)
        if user:
            user.ban(reason)
            await self.session.flush()
        return user
    
    async def unban_user(self, user_id: int) -> Optional[User]:
        """
        Unban user.
        
        Args:
            user_id: User ID
        
        Returns:
            Updated user or None
        """
        user = await self.get_by_id(user_id)
        if user:
            user.unban()
            await self.session.flush()
        return user
    
    async def set_role(
        self,
        user_id: int,
        role: UserRole,
    ) -> Optional[User]:
        """
        Set user role.
        
        Args:
            user_id: User ID
            role: New role
        
        Returns:
            Updated user or None
        """
        return await self.update(user_id, role=role)
    
    async def get_all_telegram_ids(self, is_active: bool = True) -> list[int]:
        """
        Get all user Telegram IDs (for broadcast).
        
        Args:
            is_active: Filter by active status
        
        Returns:
            List of Telegram IDs
        """
        stmt = select(User.telegram_id).where(
            User.is_active == is_active,
            User.is_banned == False,
        )
        
        result = await self.session.execute(stmt)
        return [row[0] for row in result.all()]
