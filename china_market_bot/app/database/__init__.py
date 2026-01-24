"""
🗄️ Database Package

Database configuration, models, and repositories.
"""

from .engine import create_engine, create_test_engine, engine
from .models import (
    Base,
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Payment,
    Product,
    Review,
    Seller,
    User,
)
from .repositories import (
    BaseRepository,
    CartRepository,
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from .session import (
    DatabaseSessionManager,
    async_session_factory,
    get_session,
    get_session_context,
    session_manager,
)

__all__ = [
    # Engine
    "engine",
    "create_engine",
    "create_test_engine",
    # Session
    "async_session_factory",
    "get_session",
    "get_session_context",
    "session_manager",
    "DatabaseSessionManager",
    # Base
    "Base",
    # Models
    "User",
    "Seller",
    "Category",
    "Product",
    "CartItem",
    "Cart",
    "Order",
    "OrderItem",
    "Review",
    "Payment",
    # Repositories
    "BaseRepository",
    "UserRepository",
    "ProductRepository",
    "CartRepository",
    "OrderRepository",
]
