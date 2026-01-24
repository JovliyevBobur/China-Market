"""
🔑 Admin Handlers Package

All admin-related handlers.
"""

from aiogram import Router

from app.filters.admin import AdminFilter

from . import panel, users, categories, moderation, broadcast

# Create admin router with admin filter
router = Router(name="admin")
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())

# Include all admin routers
router.include_router(panel.router)
router.include_router(users.router)
router.include_router(categories.router)
router.include_router(moderation.router)
router.include_router(broadcast.router)

__all__ = ["router"]
