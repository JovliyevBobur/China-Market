"""
🎮 Handlers Package

All bot handlers organized by role.
"""

from aiogram import Router

from .common import router as common_router
from .user import router as user_router
from .seller import router as seller_router
from .admin import router as admin_router

# Main router that includes all sub-routers
main_router = Router(name="main")

# Include routers in order of priority
# Admin first (most restrictive filters)
main_router.include_router(admin_router)
# Then seller
main_router.include_router(seller_router)
# Common handlers
main_router.include_router(common_router)
# User handlers (least restrictive)
main_router.include_router(user_router)

# Export for use in main.py
__all__ = ["main_router"]
