#!/usr/bin/env python
"""
🗄️ Database Initialization Script

Creates database tables and initial data.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine, async_session_factory
from app.database.models import Category, User
from app.config.constants import UserRole


async def create_tables():
    """Create all database tables."""
    logger.info("Creating database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Tables created successfully!")


async def create_initial_categories():
    """Create initial product categories."""
    logger.info("Creating initial categories...")
    
    categories = [
        {"name": "Elektronika", "name_uz": "Elektronika", "name_ru": "Электроника", "name_en": "Electronics", "slug": "elektronika", "icon": "📱", "sort_order": 1},
        {"name": "Kiyim-kechak", "name_uz": "Kiyim-kechak", "name_ru": "Одежда", "name_en": "Clothing", "slug": "kiyim-kechak", "icon": "👕", "sort_order": 2},
        {"name": "Uy jihozlari", "name_uz": "Uy jihozlari", "name_ru": "Товары для дома", "name_en": "Home & Garden", "slug": "uy-jihozlari", "icon": "🏠", "sort_order": 3},
        {"name": "Sport", "name_uz": "Sport", "name_ru": "Спорт", "name_en": "Sports", "slug": "sport", "icon": "⚽", "sort_order": 4},
        {"name": "Go'zallik", "name_uz": "Go'zallik", "name_ru": "Красота", "name_en": "Beauty", "slug": "gozallik", "icon": "💄", "sort_order": 5},
        {"name": "Bolalar uchun", "name_uz": "Bolalar uchun", "name_ru": "Дети", "name_en": "Kids", "slug": "bolalar", "icon": "🧸", "sort_order": 6},
        {"name": "Avtomobil", "name_uz": "Avtomobil", "name_ru": "Авто", "name_en": "Auto", "slug": "avtomobil", "icon": "🚗", "sort_order": 7},
        {"name": "Oziq-ovqat", "name_uz": "Oziq-ovqat", "name_ru": "Еда", "name_en": "Food", "slug": "oziq-ovqat", "icon": "🍎", "sort_order": 8},
    ]
    
    async with async_session_factory() as session:
        for cat_data in categories:
            # Check if exists
            result = await session.execute(
                text("SELECT id FROM categories WHERE slug = :slug"),
                {"slug": cat_data["slug"]}
            )
            if result.scalar() is None:
                category = Category(**cat_data)
                session.add(category)
        
        await session.commit()
    
    logger.info(f"Created {len(categories)} categories!")


async def alter_tables():
    """Safely apply schema updates for existing tables."""
    logger.info("Applying schema updates...")
    async with engine.begin() as conn:
        try:
            # Add external_url to products if missing
            await conn.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS external_url VARCHAR(500);"))
        except Exception as e:
            logger.warning(f"Could not apply schema updates: {e}")
            
    logger.info("Schema updates applied!")


async def main():
    """Main initialization function."""
    logger.info("=" * 50)
    logger.info("🗄️ Database Initialization")
    logger.info("=" * 50)
    logger.info(f"Database: {settings.db_name}")
    logger.info(f"Host: {settings.db_host}")
    logger.info("=" * 50)
    
    try:
        # Create tables
        await create_tables()
        
        # Apply schema updates to existing tables
        await alter_tables()
        
        # Create initial data
        await create_initial_categories()
        
        logger.info("=" * 50)
        logger.info("✅ Database initialized successfully!")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
