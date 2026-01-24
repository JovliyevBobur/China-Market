"""
👤 User Handlers Package

All user-related handlers.
"""

from aiogram import Router

from . import start, catalog, cart

# Create user router
router = Router(name="user")

# Include all user routers
router.include_router(start.router)
router.include_router(catalog.router)
router.include_router(cart.router)

__all__ = ["router"]
