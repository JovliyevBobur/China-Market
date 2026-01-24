"""
🧪 User Repository Unit Tests
"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories import UserRepository
from app.config.constants import UserRole


class TestUserRepository:
    """Tests for UserRepository."""
    
    @pytest_asyncio.fixture
    async def user_repo(self, session: AsyncSession) -> UserRepository:
        """Create user repository instance."""
        return UserRepository(session)
    
    @pytest.mark.asyncio
    async def test_create_user(self, user_repo: UserRepository, sample_user_data: dict):
        """Test creating a new user."""
        user = await user_repo.create(**sample_user_data)
        
        assert user is not None
        assert user.id is not None
        assert user.telegram_id == sample_user_data["telegram_id"]
        assert user.username == sample_user_data["username"]
        assert user.first_name == sample_user_data["first_name"]
        assert user.role == UserRole.USER
    
    @pytest.mark.asyncio
    async def test_get_by_telegram_id(self, user_repo: UserRepository, sample_user_data: dict):
        """Test getting user by Telegram ID."""
        # Create user first
        created_user = await user_repo.create(**sample_user_data)
        
        # Get by Telegram ID
        user = await user_repo.get_by_telegram_id(sample_user_data["telegram_id"])
        
        assert user is not None
        assert user.id == created_user.id
    
    @pytest.mark.asyncio
    async def test_get_by_telegram_id_not_found(self, user_repo: UserRepository):
        """Test getting non-existent user by Telegram ID."""
        user = await user_repo.get_by_telegram_id(999999999)
        
        assert user is None
    
    @pytest.mark.asyncio
    async def test_get_or_create_new_user(self, user_repo: UserRepository, sample_user_data: dict):
        """Test get_or_create with new user."""
        user, created = await user_repo.get_or_create(
            telegram_id=sample_user_data["telegram_id"],
            username=sample_user_data["username"],
            first_name=sample_user_data["first_name"],
            last_name=sample_user_data["last_name"],
        )
        
        assert user is not None
        assert created is True
    
    @pytest.mark.asyncio
    async def test_get_or_create_existing_user(self, user_repo: UserRepository, sample_user_data: dict):
        """Test get_or_create with existing user."""
        # Create user first
        await user_repo.create(**sample_user_data)
        
        # Get or create
        user, created = await user_repo.get_or_create(
            telegram_id=sample_user_data["telegram_id"],
            username="new_username",
            first_name=sample_user_data["first_name"],
            last_name=sample_user_data["last_name"],
        )
        
        assert user is not None
        assert created is False
        assert user.username == "new_username"  # Updated
    
    @pytest.mark.asyncio
    async def test_ban_user(self, user_repo: UserRepository, sample_user_data: dict):
        """Test banning a user."""
        # Create user
        created_user = await user_repo.create(**sample_user_data)
        
        # Ban user
        user = await user_repo.ban_user(created_user.id, "Test ban reason")
        
        assert user is not None
        assert user.is_banned is True
        assert user.ban_reason == "Test ban reason"
        assert user.banned_at is not None
    
    @pytest.mark.asyncio
    async def test_unban_user(self, user_repo: UserRepository, sample_user_data: dict):
        """Test unbanning a user."""
        # Create and ban user
        created_user = await user_repo.create(**sample_user_data)
        await user_repo.ban_user(created_user.id, "Test ban")
        
        # Unban user
        user = await user_repo.unban_user(created_user.id)
        
        assert user is not None
        assert user.is_banned is False
        assert user.ban_reason is None
    
    @pytest.mark.asyncio
    async def test_set_role(self, user_repo: UserRepository, sample_user_data: dict):
        """Test setting user role."""
        # Create user
        created_user = await user_repo.create(**sample_user_data)
        
        # Set role
        user = await user_repo.set_role(created_user.id, UserRole.SELLER)
        
        assert user is not None
        assert user.role == UserRole.SELLER
