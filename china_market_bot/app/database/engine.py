"""
🗄️ Database Engine Module

SQLAlchemy async engine configuration.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings


def create_engine(
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_pre_ping: bool = True,
    echo: bool = False,
) -> AsyncEngine:
    """
    Create async SQLAlchemy engine.
    
    Args:
        pool_size: The number of connections to keep open inside the pool.
        max_overflow: The number of connections to allow in overflow.
        pool_pre_ping: Enable pessimistic disconnect handling.
        echo: If True, the Engine will log all statements.
    
    Returns:
        AsyncEngine: Configured async SQLAlchemy engine
    """
    engine = create_async_engine(
        settings.database_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=pool_pre_ping,
        echo=echo or settings.debug,
        future=True,
    )
    
    return engine


def create_test_engine() -> AsyncEngine:
    """
    Create async SQLAlchemy engine for testing with NullPool.
    
    Returns:
        AsyncEngine: Configured async SQLAlchemy engine for tests
    """
    return create_async_engine(
        settings.database_url,
        poolclass=NullPool,
        echo=False,
        future=True,
    )


# Global engine instance
engine = create_engine()
