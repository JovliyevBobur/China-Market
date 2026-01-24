"""
📦 Base Repository Module

Abstract base repository with common CRUD operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.base import Base

# Generic type for models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(ABC, Generic[ModelType]):
    """
    Abstract base repository with common CRUD operations.
    
    All repositories should inherit from this class.
    """
    
    model: Type[ModelType]
    
    def __init__(self, session: AsyncSession):
        """
        Initialize repository with database session.
        
        Args:
            session: SQLAlchemy async session
        """
        self.session = session
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get record by primary key ID.
        
        Args:
            id: Primary key ID
        
        Returns:
            Model instance or None
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[Any] = None,
    ) -> Sequence[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            limit: Maximum number of records
            offset: Number of records to skip
            order_by: Column to order by
        
        Returns:
            Sequence of model instances
        """
        stmt = select(self.model)
        
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def count(self) -> int:
        """
        Count all records.
        
        Returns:
            Total record count
        """
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()
    
    async def create(self, **kwargs) -> ModelType:
        """
        Create new record.
        
        Args:
            **kwargs: Model field values
        
        Returns:
            Created model instance
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    
    async def create_many(self, items: list[dict]) -> list[ModelType]:
        """
        Create multiple records.
        
        Args:
            items: List of dictionaries with field values
        
        Returns:
            List of created model instances
        """
        instances = [self.model(**item) for item in items]
        self.session.add_all(instances)
        await self.session.flush()
        for instance in instances:
            await self.session.refresh(instance)
        return instances
    
    async def update(
        self,
        id: int,
        **kwargs,
    ) -> Optional[ModelType]:
        """
        Update record by ID.
        
        Args:
            id: Primary key ID
            **kwargs: Fields to update
        
        Returns:
            Updated model instance or None
        """
        instance = await self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            await self.session.flush()
            await self.session.refresh(instance)
        return instance
    
    async def update_many(
        self,
        conditions: dict,
        **kwargs,
    ) -> int:
        """
        Update multiple records matching conditions.
        
        Args:
            conditions: Dictionary of field conditions
            **kwargs: Fields to update
        
        Returns:
            Number of updated records
        """
        stmt = update(self.model).values(**kwargs)
        
        for key, value in conditions.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount
    
    async def delete(self, id: int) -> bool:
        """
        Delete record by ID.
        
        Args:
            id: Primary key ID
        
        Returns:
            True if deleted, False if not found
        """
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.flush()
        return result.rowcount > 0
    
    async def delete_many(self, conditions: dict) -> int:
        """
        Delete multiple records matching conditions.
        
        Args:
            conditions: Dictionary of field conditions
        
        Returns:
            Number of deleted records
        """
        stmt = delete(self.model)
        
        for key, value in conditions.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount
    
    async def exists(self, **kwargs) -> bool:
        """
        Check if record exists with given conditions.
        
        Args:
            **kwargs: Field conditions
        
        Returns:
            True if exists, False otherwise
        """
        stmt = select(func.count()).select_from(self.model)
        
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        
        result = await self.session.execute(stmt)
        return result.scalar_one() > 0
    
    async def get_one(self, **kwargs) -> Optional[ModelType]:
        """
        Get single record matching conditions.
        
        Args:
            **kwargs: Field conditions
        
        Returns:
            Model instance or None
        """
        stmt = select(self.model)
        
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_many(
        self,
        conditions: Optional[dict] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: Optional[Any] = None,
    ) -> Sequence[ModelType]:
        """
        Get multiple records matching conditions.
        
        Args:
            conditions: Dictionary of field conditions
            limit: Maximum number of records
            offset: Number of records to skip
            order_by: Column to order by
        
        Returns:
            Sequence of model instances
        """
        stmt = select(self.model)
        
        if conditions:
            for key, value in conditions.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
        
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
