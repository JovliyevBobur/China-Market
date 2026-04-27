"""
👤 User Handlers Package

All user-related handlers.
"""

from aiogram import Router

from . import start, catalog, cart, profile, orders, search, support

# Create user router
router = Router(name="user")

# Include all user routers
router.include_router(start.router)
router.include_router(catalog.router)
router.include_router(cart.router)
router.include_router(profile.router)
router.include_router(orders.router)
router.include_router(search.router)
router.include_router(support.router)

__all__ = ["router"]
