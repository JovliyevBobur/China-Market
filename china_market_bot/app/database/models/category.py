"""
📁 Category Model Module

Category database model for organizing products.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, TimestampMixin

if TYPE_CHECKING:
    from .product import Product


class Category(Base, IDMixin, TimestampMixin):
    """
    Category model for organizing products.
    
    Supports hierarchical categories (parent-child relationship).
    """
    
    __tablename__ = "categories"
    
    # Basic Info
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Category name",
    )
    name_uz: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="Category name in Uzbek",
    )
    name_ru: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="Category name in Russian",
    )
    name_en: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="Category name in English",
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Category description",
    )
    
    # URL-friendly slug
    slug: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
        comment="URL-friendly slug",
    )
    
    # Visual
    icon: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Emoji or icon name",
    )
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Category image URL",
    )
    
    # Hierarchy
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Parent category ID",
    )
    
    # Ordering
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Sort order for display",
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Is category active",
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Is category featured",
    )
    
    # SEO
    meta_title: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="SEO meta title",
    )
    meta_description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="SEO meta description",
    )
    
    # Relationships
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="children",
        remote_side="Category.id",
        lazy="selectin",
    )
    
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        lazy="selectin",
        order_by="Category.sort_order",
    )
    
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="selectin",
    )
    
    # Properties
    @property
    def is_root(self) -> bool:
        """Check if category is root (no parent)."""
        return self.parent_id is None
    
    @property
    def has_children(self) -> bool:
        """Check if category has subcategories."""
        return len(self.children) > 0
    
    @property
    def product_count(self) -> int:
        """Get active product count."""
        return len([p for p in self.products if p.is_active])
    
    @property
    def full_path(self) -> str:
        """Get full category path (Parent > Child)."""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def get_name(self, language: str = "uz") -> str:
        """Get category name in specified language."""
        if language == "ru" and self.name_ru:
            return self.name_ru
        elif language == "en" and self.name_en:
            return self.name_en
        elif language == "uz" and self.name_uz:
            return self.name_uz
        return self.name
    
    def get_all_children_ids(self) -> list[int]:
        """Get all descendant category IDs recursively."""
        ids = [self.id]
        for child in self.children:
            ids.extend(child.get_all_children_ids())
        return ids
