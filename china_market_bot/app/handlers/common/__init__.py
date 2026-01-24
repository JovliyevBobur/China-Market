"""
🔧 Common Handlers Package

Common handlers like cancel and errors.
"""

from aiogram import Router

from . import cancel, errors

router = Router(name="common")

router.include_router(cancel.router)
router.include_router(errors.router)

__all__ = ["router"]
