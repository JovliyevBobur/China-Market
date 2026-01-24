"""
👥 Admin Users Handler

User management for admins - search, ban, unban users.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.config.constants import UserRole
from app.database.models import User
from app.states.admin_states import AdminStates

router = Router(name="admin_users")


@router.callback_query(F.data == "admin:users")
async def list_users(callback: CallbackQuery, session) -> None:
    """List recent users."""
    from sqlalchemy import select, func
    
    # Count users
    stmt = select(func.count(User.id))
    result = await session.execute(stmt)
    total = result.scalar() or 0
    
    # Recent users
    stmt = select(User).order_by(User.created_at.desc()).limit(10)
    result = await session.execute(stmt)
    users = result.scalars().all()
    
    text = f"👥 <b>Foydalanuvchilar</b> ({total} ta)\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for user in users:
        status = "🚫" if user.is_banned else "👤"
        role_emoji = {"admin": "🔑", "seller": "🏪", "moderator": "👮"}.get(user.role.value, "")
        buttons.append([
            InlineKeyboardButton(
                text=f"{status}{role_emoji} {user.full_name[:20]} (@{user.username or 'no_username'})",
                callback_data=f"admin:user:{user.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="🔍 Qidirish", callback_data="admin:search_user"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:panel"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("admin:user:"))
async def view_user(callback: CallbackQuery, session) -> None:
    """View user details."""
    from sqlalchemy import select
    
    user_id = int(callback.data.split(":")[2])
    
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        await callback.answer("❌ Foydalanuvchi topilmadi!", show_alert=True)
        return
    
    status = "🚫 Bloklangan" if user.is_banned else "✅ Faol"
    role_names = {
        UserRole.USER: "👤 Foydalanuvchi",
        UserRole.SELLER: "🏪 Sotuvchi",
        UserRole.MODERATOR: "👮 Moderator",
        UserRole.ADMIN: "🔑 Admin",
    }
    
    text = (
        f"👤 <b>{user.full_name}</b>\n\n"
        f"🆔 ID: <code>{user.telegram_id}</code>\n"
        f"👤 Username: @{user.username or 'yo\\'q'}\n"
        f"📱 Telefon: {user.phone or 'Noma\\'lum'}\n"
        f"🌍 Til: {user.language}\n"
        f"👔 Rol: {role_names.get(user.role, user.role.value)}\n"
        f"📌 Holat: {status}\n"
        f"📅 Ro'yxatdan: {user.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"🕐 Oxirgi faollik: {user.last_activity.strftime('%d.%m.%Y %H:%M')}\n"
    )
    
    if user.is_banned:
        text += f"\n⛔ Ban sababi: {user.ban_reason or 'Noma\\'lum'}\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    
    if user.is_banned:
        buttons.append([
            InlineKeyboardButton(text="✅ Unban", callback_data=f"admin:unban:{user.id}"),
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="🚫 Ban", callback_data=f"admin:ban:{user.id}"),
        ])
    
    # Change role
    buttons.append([
        InlineKeyboardButton(text="👔 Rol o'zgartirish", callback_data=f"admin:change_role:{user.id}"),
    ])
    
    buttons.append([
        InlineKeyboardButton(text="💬 Xabar yuborish", callback_data=f"admin:message_user:{user.id}"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:users"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("admin:ban:"))
async def ban_user_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Start ban process."""
    user_id = callback.data.split(":")[2]
    await state.update_data(ban_user_id=user_id)
    await state.set_state(AdminStates.user_ban_reason)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"admin:user:{user_id}")],
    ])
    
    await callback.message.edit_text(
        "🚫 <b>Foydalanuvchini bloklash</b>\n\n"
        "Ban sababini kiriting:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(AdminStates.user_ban_reason)
async def process_ban(message: Message, session, state: FSMContext) -> None:
    """Process user ban."""
    from sqlalchemy import select
    from app.loader import bot
    
    data = await state.get_data()
    user_id = int(data['ban_user_id'])
    reason = message.text
    
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi!")
        await state.clear()
        return
    
    user.ban(reason)
    await session.commit()
    
    # Notify user
    try:
        await bot.send_message(
            chat_id=user.telegram_id,
            text=f"🚫 <b>Siz bloklangansiz!</b>\n\n"
                 f"Sabab: {reason}\n\n"
                 f"Agar bu xato bo'lsa, admin bilan bog'laning.",
        )
    except Exception:
        pass
    
    await state.clear()
    
    await message.answer(f"✅ Foydalanuvchi bloklandi!\n\nSabab: {reason}")


@router.callback_query(F.data.startswith("admin:unban:"))
async def unban_user(callback: CallbackQuery, session) -> None:
    """Unban user."""
    from sqlalchemy import select
    from app.loader import bot
    
    user_id = int(callback.data.split(":")[2])
    
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        await callback.answer("❌ Foydalanuvchi topilmadi!", show_alert=True)
        return
    
    user.unban()
    await session.commit()
    
    # Notify user
    try:
        await bot.send_message(
            chat_id=user.telegram_id,
            text="✅ <b>Sizning blokingiz olib tashlandi!</b>\n\n"
                 "Botdan foydalanishingiz mumkin.",
        )
    except Exception:
        pass
    
    await callback.answer("✅ Foydalanuvchi blokdan chiqarildi!")
    await view_user(callback, session)


@router.callback_query(F.data == "admin:search_user")
async def search_user_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Start user search."""
    await state.set_state(AdminStates.user_search)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:users")],
    ])
    
    await callback.message.edit_text(
        "🔍 <b>Foydalanuvchi qidirish</b>\n\n"
        "Username, telefon yoki ID ni kiriting:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(AdminStates.user_search)
async def process_search(message: Message, session, state: FSMContext) -> None:
    """Process user search."""
    from sqlalchemy import select, or_
    
    query = message.text.strip()
    await state.clear()
    
    # Search by different fields
    conditions = [
        User.username.ilike(f"%{query}%"),
        User.first_name.ilike(f"%{query}%"),
        User.phone.ilike(f"%{query}%"),
    ]
    
    # Try to search by ID
    try:
        user_id = int(query)
        conditions.append(User.telegram_id == user_id)
    except ValueError:
        pass
    
    stmt = select(User).where(or_(*conditions)).limit(10)
    result = await session.execute(stmt)
    users = result.scalars().all()
    
    if not users:
        await message.answer(
            f"❌ '{query}' bo'yicha foydalanuvchi topilmadi.",
        )
        return
    
    text = f"🔍 <b>Qidiruv natijalari</b> ({len(users)} ta)\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for user in users:
        buttons.append([
            InlineKeyboardButton(
                text=f"👤 {user.full_name} (@{user.username or 'no'})",
                callback_data=f"admin:user:{user.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:users"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await message.answer(text, reply_markup=keyboard)
