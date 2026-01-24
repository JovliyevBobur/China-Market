"""
🗄️ Database Session Module

AsyncSession factory and context manager.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .engine import engine


# Session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session as async generator.
    
    This is used as a dependency in handlers.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session as async context manager.
    
    This is used for manual session management.
    
    Yields:
        AsyncSession: Database session
    
    Example:
        async with get_session_context() as session:
            user = await session.get(User, user_id)
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class DatabaseSessionManager:
    """
    Database session manager for handling lifecycle.
    
    Provides methods for creating and closing database connections.
    """
    
    def __init__(self):
        self._session_factory = async_session_factory
    
    async def close(self) -> None:
        """Close all database connections."""
        await engine.dispose()
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get database session.
        
        Yields:
            AsyncSession: Database session
        """
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global session manager
session_manager = DatabaseSessionManager()
