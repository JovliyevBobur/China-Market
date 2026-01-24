"""
🏪 Seller Handlers Package

All seller-related handlers.
"""

from aiogram import Router

from . import dashboard, products, orders, analytics

# Create seller router
router = Router(name="seller")

# Include all seller routers
router.include_router(dashboard.router)
router.include_router(products.router)
router.include_router(orders.router)
router.include_router(analytics.router)

__all__ = ["router"]
