"""
🔑 Admin Panel Handler

Main admin dashboard with statistics and quick actions.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.config.constants import OrderStatus, UserRole
from app.database.models import User, Product, Order, Seller

router = Router(name="admin_panel")


@router.message(Command("admin"))
async def admin_panel(message: Message, user: User, session) -> None:
    """Show admin panel."""
    from sqlalchemy import select, func
    
    # Get statistics
    # Total users
    stmt = select(func.count(User.id))
    result = await session.execute(stmt)
    total_users = result.scalar() or 0
    
    # Total sellers
    stmt = select(func.count(Seller.id))
    result = await session.execute(stmt)
    total_sellers = result.scalar() or 0
    
    # Total products
    stmt = select(func.count(Product.id))
    result = await session.execute(stmt)
    total_products = result.scalar() or 0
    
    # Pending moderation
    from app.config.constants import ModerationStatus
    stmt = select(func.count(Product.id)).where(Product.is_approved == False)
    result = await session.execute(stmt)
    pending_products = result.scalar() or 0
    
    # Total orders
    stmt = select(func.count(Order.id))
    result = await session.execute(stmt)
    total_orders = result.scalar() or 0
    
    # Pending orders
    stmt = select(func.count(Order.id)).where(Order.status == OrderStatus.PENDING)
    result = await session.execute(stmt)
    pending_orders = result.scalar() or 0
    
    # Total revenue
    stmt = select(func.sum(Order.total_amount)).where(Order.status == OrderStatus.DELIVERED)
    result = await session.execute(stmt)
    total_revenue = result.scalar() or 0
    
    text = (
        f"🔑 <b>Admin Panel</b>\n\n"
        f"📊 <b>Statistika:</b>\n"
        f"├ 👥 Foydalanuvchilar: {total_users} ta\n"
        f"├ 🏪 Sotuvchilar: {total_sellers} ta\n"
        f"├ 📦 Mahsulotlar: {total_products} ta\n"
        f"├ 📋 Buyurtmalar: {total_orders} ta\n"
        f"└ 💰 Daromad: {total_revenue:,.0f} so'm\n\n"
        f"⚠️ <b>E'tiborga:</b>\n"
        f"├ ⏳ Moderatsiyada: {pending_products} ta mahsulot\n"
        f"└ ⏳ Yangi buyurtmalar: {pending_orders} ta\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin:users"),
            InlineKeyboardButton(text="🏪 Sotuvchilar", callback_data="admin:sellers"),
        ],
        [
            InlineKeyboardButton(text="📦 Moderatsiya", callback_data="admin:moderation"),
            InlineKeyboardButton(text="📂 Kategoriyalar", callback_data="admin:categories"),
        ],
        [
            InlineKeyboardButton(text="📢 Xabar tarqatish", callback_data="admin:broadcast"),
        ],
        [
            InlineKeyboardButton(text="📊 Batafsil statistika", callback_data="admin:stats"),
        ],
    ])
    
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "admin:panel")
async def admin_panel_callback(callback: CallbackQuery, user: User, session) -> None:
    """Show admin panel (callback)."""
    from sqlalchemy import select, func
    
    # Total users
    stmt = select(func.count(User.id))
    result = await session.execute(stmt)
    total_users = result.scalar() or 0
    
    # Pending moderation
    stmt = select(func.count(Product.id)).where(Product.is_approved == False)
    result = await session.execute(stmt)
    pending_products = result.scalar() or 0
    
    text = (
        f"🔑 <b>Admin Panel</b>\n\n"
        f"👥 Foydalanuvchilar: {total_users} ta\n"
        f"⏳ Moderatsiyada: {pending_products} ta\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin:users"),
            InlineKeyboardButton(text="🏪 Sotuvchilar", callback_data="admin:sellers"),
        ],
        [
            InlineKeyboardButton(text="📦 Moderatsiya", callback_data="admin:moderation"),
            InlineKeyboardButton(text="📂 Kategoriyalar", callback_data="admin:categories"),
        ],
        [
            InlineKeyboardButton(text="📢 Xabar tarqatish", callback_data="admin:broadcast"),
        ],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "admin:stats")
async def detailed_stats(callback: CallbackQuery, session) -> None:
    """Show detailed statistics."""
    from sqlalchemy import select, func
    from datetime import datetime, timedelta
    
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Today's users
    stmt = select(func.count(User.id)).where(
        func.date(User.created_at) == today
    )
    result = await session.execute(stmt)
    today_users = result.scalar() or 0
    
    # This week users
    stmt = select(func.count(User.id)).where(User.created_at >= week_ago)
    result = await session.execute(stmt)
    week_users = result.scalar() or 0
    
    # This month orders
    stmt = select(func.count(Order.id)).where(Order.created_at >= month_ago)
    result = await session.execute(stmt)
    month_orders = result.scalar() or 0
    
    # This month revenue
    stmt = select(func.sum(Order.total_amount)).where(
        Order.status == OrderStatus.DELIVERED,
        Order.created_at >= month_ago,
    )
    result = await session.execute(stmt)
    month_revenue = result.scalar() or 0
    
    text = (
        f"📊 <b>Batafsil statistika</b>\n\n"
        f"👥 <b>Foydalanuvchilar:</b>\n"
        f"├ Bugun: +{today_users} ta\n"
        f"├ Bu hafta: +{week_users} ta\n\n"
        f"📋 <b>Buyurtmalar:</b>\n"
        f"├ Bu oy: {month_orders} ta\n\n"
        f"💰 <b>Daromad:</b>\n"
        f"└ Bu oy: {month_revenue:,.0f} so'm\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:panel")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "admin:sellers")
async def list_sellers(callback: CallbackQuery, session) -> None:
    """List all sellers."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    stmt = (
        select(Seller)
        .order_by(Seller.created_at.desc())
        .limit(20)
        .options(selectinload(Seller.user))
    )
    result = await session.execute(stmt)
    sellers = result.scalars().all()
    
    if not sellers:
        await callback.answer("Sotuvchilar yo'q!", show_alert=True)
        return
    
    # Count pending
    pending = sum(1 for s in sellers if not s.is_verified)
    
    text = f"🏪 <b>Sotuvchilar</b> ({len(sellers)} ta)\n\n"
    text += f"⏳ Tasdiqlash kutmoqda: {pending} ta\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for seller in sellers[:8]:
        status = "✅" if seller.is_verified else "⏳"
        buttons.append([
            InlineKeyboardButton(
                text=f"{status} {seller.company_name[:25]}",
                callback_data=f"admin:seller:{seller.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⏳ Tasdiqlash kutmoqda", callback_data="admin:pending_sellers"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:panel"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("admin:seller:"))
async def view_seller(callback: CallbackQuery, session) -> None:
    """View seller details."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    seller_id = int(callback.data.split(":")[2])
    
    stmt = select(Seller).where(Seller.id == seller_id).options(selectinload(Seller.user))
    result = await session.execute(stmt)
    seller = result.scalar_one_or_none()
    
    if not seller:
        await callback.answer("❌ Sotuvchi topilmadi!", show_alert=True)
        return
    
    status = "✅ Tasdiqlangan" if seller.is_verified else "⏳ Kutilmoqda"
    
    text = (
        f"🏪 <b>{seller.company_name}</b>\n\n"
        f"👤 Egasi: {seller.user.full_name}\n"
        f"📱 Telefon: {seller.phone or 'Noma\\'lum'}\n"
        f"📧 Email: {seller.email or 'Noma\\'lum'}\n"
        f"📍 Manzil: {seller.address or 'Kiritilmagan'}\n\n"
        f"📌 Holat: {status}\n"
        f"📅 Ro'yxatdan o'tgan: {seller.created_at.strftime('%d.%m.%Y')}\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    
    if not seller.is_verified:
        buttons.append([
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"admin:approve_seller:{seller.id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"admin:reject_seller:{seller.id}"),
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="🚫 Bloklash", callback_data=f"admin:block_seller:{seller.id}"),
        ])
    
    buttons.append([
        InlineKeyboardButton(text="📦 Mahsulotlari", callback_data=f"admin:seller_products:{seller.id}"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:sellers"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("admin:approve_seller:"))
async def approve_seller(callback: CallbackQuery, session) -> None:
    """Approve seller."""
    from sqlalchemy import select
    from app.loader import bot
    
    seller_id = int(callback.data.split(":")[2])
    
    stmt = select(Seller).where(Seller.id == seller_id)
    result = await session.execute(stmt)
    seller = result.scalar_one_or_none()
    
    if not seller:
        await callback.answer("❌ Sotuvchi topilmadi!", show_alert=True)
        return
    
    seller.is_verified = True
    seller.verified_at = __import__('datetime').datetime.utcnow()
    
    # Update user role
    from sqlalchemy import update
    stmt = update(User).where(User.id == seller.user_id).values(role=UserRole.SELLER)
    await session.execute(stmt)
    
    await session.commit()
    
    # Notify seller
    try:
        await bot.send_message(
            chat_id=seller.user_id_telegram,
            text="🎉 <b>Tabriklaymiz!</b>\n\n"
                 "Sizning sotuvchi arizangiz tasdiqlandi!\n"
                 "Endi mahsulotlar qo'shishingiz mumkin.\n\n"
                 "/seller - Sotuvchi paneliga o'tish",
        )
    except Exception:
        pass
    
    await callback.answer("✅ Sotuvchi tasdiqlandi!")
    await view_seller(callback, session)
