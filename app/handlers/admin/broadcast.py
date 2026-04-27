"""
📢 Admin Broadcast Handler

Mass messaging to users.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.database.models import User
from app.states.admin_states import AdminStates

router = Router(name="admin_broadcast")


@router.callback_query(F.data == "admin:broadcast")
async def start_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    """Start broadcast process."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Barcha foydalanuvchilarga", callback_data="broadcast:all")],
        [InlineKeyboardButton(text="🏪 Faqat sotuvchilarga", callback_data="broadcast:sellers")],
        [InlineKeyboardButton(text="👤 Faqat xaridorlarga", callback_data="broadcast:users")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:panel")],
    ])
    
    await callback.message.edit_text(
        "📢 <b>Xabar tarqatish</b>\n\n"
        "Kimga xabar yuborishni tanlang:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("broadcast:"))
async def select_audience(callback: CallbackQuery, state: FSMContext, session) -> None:
    """Select broadcast audience."""
    from sqlalchemy import select, func
    from app.config.constants import UserRole
    
    audience = callback.data.split(":")[1]
    
    # Count users
    if audience == "all":
        stmt = select(func.count(User.id)).where(User.is_banned == False)
        target = "barcha foydalanuvchilar"
    elif audience == "sellers":
        stmt = select(func.count(User.id)).where(
            User.is_banned == False,
            User.role == UserRole.SELLER,
        )
        target = "sotuvchilar"
    else:
        stmt = select(func.count(User.id)).where(
            User.is_banned == False,
            User.role == UserRole.USER,
        )
        target = "xaridorlar"
    
    result = await session.execute(stmt)
    count = result.scalar() or 0
    
    await state.update_data(audience=audience, target_count=count)
    await state.set_state(AdminStates.broadcast_message)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:panel")],
    ])
    
    await callback.message.edit_text(
        f"📢 <b>Xabar tarqatish</b>\n\n"
        f"👥 Maqsad: {target} ({count} ta)\n\n"
        f"Xabar matnini kiriting:\n"
        f"<i>Rasm yuborish ham mumkin</i>",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(AdminStates.broadcast_message)
async def process_broadcast_message(message: Message, state: FSMContext) -> None:
    """Process broadcast message."""
    data = await state.get_data()
    
    # Save message data
    content_type = "photo" if message.photo else "text"
    
    if content_type == "photo":
        await state.update_data(
            content_type="photo",
            photo=message.photo[-1].file_id,
            text=message.caption or "",
        )
    else:
        await state.update_data(
            content_type="text",
            text=message.text,
        )
    
    await state.set_state(AdminStates.broadcast_confirm)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yuborish", callback_data="broadcast:confirm"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="broadcast:cancel"),
        ],
    ])
    
    preview = message.text or message.caption or "Rasm"
    
    await message.answer(
        f"📢 <b>Xabar ko'rib chiqish</b>\n\n"
        f"👥 Qabul qiluvchilar: {data['target_count']} ta\n\n"
        f"💬 <b>Xabar:</b>\n{preview[:300]}...\n\n"
        f"Yuborishni tasdiqlaysizmi?",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "broadcast:confirm", AdminStates.broadcast_confirm)
async def confirm_broadcast(callback: CallbackQuery, session, state: FSMContext) -> None:
    """Confirm and send broadcast."""
    import asyncio
    from sqlalchemy import select
    from app.loader import bot
    from app.config.constants import UserRole
    
    data = await state.get_data()
    audience = data['audience']
    content_type = data.get('content_type', 'text')
    text = data.get('text', '')
    photo = data.get('photo')
    
    await state.clear()
    
    # Get users
    if audience == "all":
        stmt = select(User.telegram_id).where(User.is_banned == False)
    elif audience == "sellers":
        stmt = select(User.telegram_id).where(
            User.is_banned == False,
            User.role == UserRole.SELLER,
        )
    else:
        stmt = select(User.telegram_id).where(
            User.is_banned == False,
            User.role == UserRole.USER,
        )
    
    result = await session.execute(stmt)
    user_ids = [row[0] for row in result.fetchall()]
    
    await callback.message.edit_text(
        f"📢 <b>Xabar yuborilmoqda...</b>\n\n"
        f"👥 Jami: {len(user_ids)} ta\n"
        f"⏳ Iltimos, kuting...",
    )
    
    # Send messages
    success = 0
    failed = 0
    
    for user_id in user_ids:
        try:
            if content_type == "photo" and photo:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=text,
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                )
            success += 1
        except Exception:
            failed += 1
        
        # Rate limiting
        await asyncio.sleep(0.05)
    
    await callback.message.edit_text(
        f"📢 <b>Xabar yuborildi!</b>\n\n"
        f"✅ Muvaffaqiyatli: {success} ta\n"
        f"❌ Muvaffaqiyatsiz: {failed} ta\n\n"
        f"Jami: {len(user_ids)} ta foydalanuvchi",
    )
    await callback.answer()


@router.callback_query(F.data == "broadcast:cancel")
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel broadcast."""
    await state.clear()
    
    await callback.message.edit_text("❌ Xabar tarqatish bekor qilindi.")
    await callback.answer()
