"""
📦 Product Repository Module

Repository for product-related database operations.
"""

from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.config.constants import ModerationStatus
from app.database.models import Category, Product

from .base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Product repository with specialized queries.
    """
    
    model = Product
    
    async def get_by_id_with_relations(self, id: int) -> Optional[Product]:
        """
        Get product with all relations loaded.
        
        Args:
            id: Product ID
        
        Returns:
            Product with relations or None
        """
        result = await self.session.execute(
            select(Product)
            .options(
                selectinload(Product.seller),
                selectinload(Product.category),
                selectinload(Product.reviews),
            )
            .where(Product.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_slug(self, slug: str) -> Optional[Product]:
        """
        Get product by slug.
        
        Args:
            slug: Product slug
        
        Returns:
            Product or None
        """
        result = await self.session.execute(
            select(Product).where(Product.slug == slug)
        )
        return result.scalar_one_or_none()
    
    async def get_by_seller(
        self,
        seller_id: int,
        limit: int = 50,
        offset: int = 0,
        is_active: Optional[bool] = None,
    ) -> Sequence[Product]:
        """
        Get products by seller.
        
        Args:
            seller_id: Seller ID
            limit: Maximum number of records
            offset: Number of records to skip
            is_active: Filter by active status
        
        Returns:
            Sequence of products
        """
        stmt = select(Product).where(Product.seller_id == seller_id)
        
        if is_active is not None:
            stmt = stmt.where(Product.is_active == is_active)
        
        stmt = stmt.order_by(Product.created_at.desc())
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_category(
        self,
        category_id: int,
        limit: int = 20,
        offset: int = 0,
        include_children: bool = True,
    ) -> Sequence[Product]:
        """
        Get products by category.
        
        Args:
            category_id: Category ID
            limit: Maximum number of records
            offset: Number of records to skip
            include_children: Include products from child categories
        
        Returns:
            Sequence of products
        """
        category_ids = [category_id]
        
        if include_children:
            # Get all child category IDs
            category = await self.session.get(Category, category_id)
            if category:
                category_ids = category.get_all_children_ids()
        
        stmt = (
            select(Product)
            .where(
                Product.category_id.in_(category_ids),
                Product.is_active == True,
                Product.moderation_status == ModerationStatus.APPROVED,
            )
            .order_by(Product.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def search(
        self,
        query: str,
        category_id: Optional[int] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        seller_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Sequence[Product]:
        """
        Search products with filters.
        
        Args:
            query: Search query
            category_id: Filter by category
            min_price: Minimum price
            max_price: Maximum price
            seller_id: Filter by seller
            limit: Maximum number of records
            offset: Number of records to skip
        
        Returns:
            Sequence of matching products
        """
        search_pattern = f"%{query}%"
        
        stmt = select(Product).where(
            Product.is_active == True,
            Product.moderation_status == ModerationStatus.APPROVED,
            (Product.name.ilike(search_pattern)) |
            (Product.description.ilike(search_pattern))
        )
        
        if category_id:
            stmt = stmt.where(Product.category_id == category_id)
        
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
        
        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)
        
        if seller_id:
            stmt = stmt.where(Product.seller_id == seller_id)
        
        stmt = stmt.order_by(Product.sold_count.desc())
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_featured(self, limit: int = 10) -> Sequence[Product]:
        """
        Get featured products.
        
        Args:
            limit: Maximum number of records
        
        Returns:
            Sequence of featured products
        """
        result = await self.session.execute(
            select(Product)
            .where(
                Product.is_active == True,
                Product.is_featured == True,
                Product.moderation_status == ModerationStatus.APPROVED,
            )
            .order_by(Product.rating.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_popular(self, limit: int = 10) -> Sequence[Product]:
        """
        Get popular products by sales.
        
        Args:
            limit: Maximum number of records
        
        Returns:
            Sequence of popular products
        """
        result = await self.session.execute(
            select(Product)
            .where(
                Product.is_active == True,
                Product.moderation_status == ModerationStatus.APPROVED,
            )
            .order_by(Product.sold_count.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_new(self, limit: int = 10) -> Sequence[Product]:
        """
        Get newest products.
        
        Args:
            limit: Maximum number of records
        
        Returns:
            Sequence of new products
        """
        result = await self.session.execute(
            select(Product)
            .where(
                Product.is_active == True,
                Product.moderation_status == ModerationStatus.APPROVED,
            )
            .order_by(Product.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_discounted(self, limit: int = 10) -> Sequence[Product]:
        """
        Get products with discounts.
        
        Args:
            limit: Maximum number of records
        
        Returns:
            Sequence of discounted products
        """
        result = await self.session.execute(
            select(Product)
            .where(
                Product.is_active == True,
                Product.moderation_status == ModerationStatus.APPROVED,
                Product.discount_price.isnot(None),
                Product.discount_price < Product.price,
            )
            .order_by(Product.discount_percent.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_pending_moderation(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Product]:
        """
        Get products pending moderation.
        
        Args:
            limit: Maximum number of records
            offset: Number of records to skip
        
        Returns:
            Sequence of pending products
        """
        result = await self.session.execute(
            select(Product)
            .where(Product.moderation_status == ModerationStatus.PENDING)
            .order_by(Product.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
    
    async def approve(
        self,
        product_id: int,
        moderator_id: int,
    ) -> Optional[Product]:
        """
        Approve product.
        
        Args:
            product_id: Product ID
            moderator_id: Moderator user ID
        
        Returns:
            Updated product or None
        """
        from datetime import datetime

        return await self.update(
            product_id,
            moderation_status=ModerationStatus.APPROVED,
            moderated_at=datetime.utcnow(),
            moderated_by=moderator_id,
            rejection_reason=None,
        )
    
    async def reject(
        self,
        product_id: int,
        moderator_id: int,
        reason: str,
    ) -> Optional[Product]:
        """
        Reject product.
        
        Args:
            product_id: Product ID
            moderator_id: Moderator user ID
            reason: Rejection reason
        
        Returns:
            Updated product or None
        """
        from datetime import datetime

        return await self.update(
            product_id,
            moderation_status=ModerationStatus.REJECTED,
            moderated_at=datetime.utcnow(),
            moderated_by=moderator_id,
            rejection_reason=reason,
        )
    
    async def increment_view(self, product_id: int) -> None:
        """
        Increment product view count.
        
        Args:
            product_id: Product ID
        """
        product = await self.get_by_id(product_id)
        if product:
            product.increment_view()
            await self.session.flush()
    
    async def count_by_category(self, category_id: int) -> int:
        """
        Count products in category.
        
        Args:
            category_id: Category ID
        
        Returns:
            Product count
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(Product)
            .where(
                Product.category_id == category_id,
                Product.is_active == True,
            )
        )
        return result.scalar_one()
    
    async def count_by_seller(self, seller_id: int) -> int:
        """
        Count products by seller.
        
        Args:
            seller_id: Seller ID
        
        Returns:
            Product count
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(Product)
            .where(Product.seller_id == seller_id)
        )
        return result.scalar_one()
