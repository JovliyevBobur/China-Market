"""
📋 Orders Handler Module

User orders history and management.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.config.constants import OrderStatus
from app.database.models import Order, User
from app.keyboards.inline.pagination import create_pagination_keyboard

router = Router(name="orders")


@router.message(Command("orders"))
@router.message(F.text.in_(["📋 Buyurtmalarim", "📋 Мои заказы", "📋 My Orders"]))
async def show_orders(message: Message, user: User, session) -> None:
    """Show user orders list."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    # Get user orders
    stmt = (
        select(Order)
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    orders = result.scalars().all()
    
    if not orders:
        await message.answer(
            "📋 <b>Buyurtmalarim</b>\n\n"
            "Sizda hali buyurtmalar yo'q.\n"
            "🛒 Mahsulotlarni ko'rish uchun /catalog buyrug'ini yuboring."
        )
        return
    
    text = "📋 <b>Sizning buyurtmalaringiz:</b>\n\n"
    
    status_emojis = {
        OrderStatus.PENDING: "⏳",
        OrderStatus.CONFIRMED: "✅",
        OrderStatus.PROCESSING: "📦",
        OrderStatus.SHIPPED: "🚚",
        OrderStatus.DELIVERED: "🎉",
        OrderStatus.CANCELLED: "❌",
        OrderStatus.REFUNDED: "💰",
    }
    
    status_names = {
        OrderStatus.PENDING: "Kutilmoqda",
        OrderStatus.CONFIRMED: "Tasdiqlangan",
        OrderStatus.PROCESSING: "Tayyorlanmoqda",
        OrderStatus.SHIPPED: "Yetkazilmoqda",
        OrderStatus.DELIVERED: "Yetkazildi",
        OrderStatus.CANCELLED: "Bekor qilindi",
        OrderStatus.REFUNDED: "Qaytarildi",
    }
    
    for order in orders:
        emoji = status_emojis.get(order.status, "📋")
        status_name = status_names.get(order.status, order.status.value)
        
        text += (
            f"{emoji} <b>#{order.id}</b> - {status_name}\n"
            f"   💰 {order.total_amount:,.0f} so'm\n"
            f"   📅 {order.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📋 Buyurtma #{o.id}", callback_data=f"order:view:{o.id}")]
        for o in orders[:5]
    ] + [
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")]
    ])
    
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("order:view:"))
async def view_order(callback: CallbackQuery, user: User, session) -> None:
    """View order details."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    order_id = int(callback.data.split(":")[2])
    
    # Get order with items
    stmt = (
        select(Order)
        .where(Order.id == order_id, Order.user_id == user.id)
        .options(selectinload(Order.items))
    )
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        await callback.answer("❌ Buyurtma topilmadi!", show_alert=True)
        return
    
    status_names = {
        OrderStatus.PENDING: "⏳ Kutilmoqda",
        OrderStatus.CONFIRMED: "✅ Tasdiqlangan",
        OrderStatus.PROCESSING: "📦 Tayyorlanmoqda",
        OrderStatus.SHIPPED: "🚚 Yetkazilmoqda",
        OrderStatus.DELIVERED: "🎉 Yetkazildi",
        OrderStatus.CANCELLED: "❌ Bekor qilindi",
        OrderStatus.REFUNDED: "💰 Qaytarildi",
    }
    
    text = (
        f"📋 <b>Buyurtma #{order.id}</b>\n\n"
        f"📊 Holat: {status_names.get(order.status, order.status.value)}\n"
        f"📅 Sana: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"📍 Manzil: {order.shipping_address or 'Kiritilmagan'}\n\n"
        f"<b>Mahsulotlar:</b>\n"
    )
    
    for item in order.items:
        text += f"  • {item.product_name} x{item.quantity} = {item.total:,.0f} so'm\n"
    
    text += (
        f"\n💰 <b>Jami: {order.total_amount:,.0f} so'm</b>\n"
        f"🚚 Yetkazish: {order.shipping_cost:,.0f} so'm\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    
    # Can cancel if pending
    if order.status == OrderStatus.PENDING:
        buttons.append([
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"order:cancel:{order.id}")
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="orders:list")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("order:cancel:"))
async def cancel_order(callback: CallbackQuery, user: User, session) -> None:
    """Cancel pending order."""
    from sqlalchemy import select
    
    order_id = int(callback.data.split(":")[2])
    
    # Get order
    stmt = select(Order).where(Order.id == order_id, Order.user_id == user.id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        await callback.answer("❌ Buyurtma topilmadi!", show_alert=True)
        return
    
    if order.status != OrderStatus.PENDING:
        await callback.answer("❌ Bu buyurtmani bekor qilib bo'lmaydi!", show_alert=True)
        return
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha, bekor qilish", callback_data=f"order:confirm_cancel:{order.id}"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data=f"order:view:{order.id}"),
        ]
    ])
    
    await callback.message.edit_text(
        f"❓ <b>Buyurtma #{order.id}</b> ni bekor qilishni xohlaysizmi?\n\n"
        f"💰 Jami: {order.total_amount:,.0f} so'm",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order:confirm_cancel:"))
async def confirm_cancel_order(callback: CallbackQuery, user: User, session) -> None:
    """Confirm order cancellation."""
    from sqlalchemy import select
    from app.loader import bot
    from app.config import settings
    
    order_id = int(callback.data.split(":")[2])
    
    # Get order
    stmt = select(Order).where(Order.id == order_id, Order.user_id == user.id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order or order.status != OrderStatus.PENDING:
        await callback.answer("❌ Bu buyurtmani bekor qilib bo'lmaydi!", show_alert=True)
        return
    
    # Cancel order
    order.status = OrderStatus.CANCELLED
    order.cancelled_at = __import__('datetime').datetime.utcnow()
    order.cancel_reason = "Foydalanuvchi tomonidan bekor qilindi"
    
    await session.commit()
    
    # Notify admins
    for admin_id in settings.admin_ids[:3]:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=f"❌ <b>Buyurtma bekor qilindi!</b>\n\n"
                     f"📋 Buyurtma: #{order.id}\n"
                     f"👤 Foydalanuvchi: {user.full_name}\n"
                     f"💰 Summa: {order.total_amount:,.0f} so'm",
            )
        except Exception:
            pass
    
    await callback.message.edit_text(
        f"✅ Buyurtma #{order.id} bekor qilindi!",
    )
    await callback.answer()


@router.callback_query(F.data == "orders:list")
async def orders_list_callback(callback: CallbackQuery, user: User, session) -> None:
    """Go back to orders list."""
    from sqlalchemy import select
    
    # Get user orders
    stmt = (
        select(Order)
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    orders = result.scalars().all()
    
    if not orders:
        await callback.message.edit_text(
            "📋 <b>Buyurtmalarim</b>\n\n"
            "Sizda hali buyurtmalar yo'q."
        )
        await callback.answer()
        return
    
    text = "📋 <b>Sizning buyurtmalaringiz:</b>\n\n"
    
    for order in orders:
        text += f"📋 <b>#{order.id}</b> - {order.status.value} - {order.total_amount:,.0f} so'm\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📋 Buyurtma #{o.id}", callback_data=f"order:view:{o.id}")]
        for o in orders[:5]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
