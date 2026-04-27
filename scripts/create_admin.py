#!/usr/bin/env python
"""
👑 Create Admin Script

Creates an admin user in the database.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

from app.config import settings
from app.config.constants import UserRole
from app.database import async_session_factory
from app.database.repositories import UserRepository


async def create_admin(
    telegram_id: int,
    username: str = None,
    first_name: str = "Admin",
):
    """
    Create admin user.
    
    Args:
        telegram_id: Admin's Telegram ID
        username: Admin's username
        first_name: Admin's first name
    """
    async with async_session_factory() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        user = await user_repo.get_by_telegram_id(telegram_id)
        
        if user:
            # Update role to admin
            user.role = UserRole.ADMIN
            logger.info(f"Updated user {telegram_id} to admin role")
        else:
            # Create new admin user
            user = await user_repo.create(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                role=UserRole.ADMIN,
                is_verified=True,
            )
            logger.info(f"Created admin user: {telegram_id}")
        
        await session.commit()
        
        return user


async def main():
    """Main function."""
    logger.info("=" * 50)
    logger.info("👑 Create Admin User")
    logger.info("=" * 50)
    
    # Get admin IDs from settings
    admin_ids = settings.admin_ids
    
    if not admin_ids:
        logger.warning("No admin IDs configured in .env file!")
        telegram_id = input("Enter admin Telegram ID: ")
        
        try:
            telegram_id = int(telegram_id)
        except ValueError:
            logger.error("Invalid Telegram ID!")
            return
        
        admin_ids = [telegram_id]
    
    for i, admin_id in enumerate(admin_ids):
        role = UserRole.SUPERADMIN if i == 0 else UserRole.ADMIN
        
        async with async_session_factory() as session:
            user_repo = UserRepository(session)
            
            user = await user_repo.get_by_telegram_id(admin_id)
            
            if user:
                user.role = role
                logger.info(f"Updated user {admin_id} to {role.value} role")
            else:
                user = await user_repo.create(
                    telegram_id=admin_id,
                    role=role,
                    is_verified=True,
                )
                logger.info(f"Created {role.value} user: {admin_id}")
            
            await session.commit()
    
    logger.info("=" * 50)
    logger.info("✅ Admin users created/updated!")
    logger.info("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
