"""
📋 Seller Orders Handler

Order management for sellers - view, process, ship orders.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.config.constants import OrderStatus
from app.database.models import User, Seller, Order
from app.filters.seller import SellerFilter

router = Router(name="seller_orders")
router.message.filter(SellerFilter())
router.callback_query.filter(SellerFilter())


@router.callback_query(F.data == "seller:orders")
async def list_seller_orders(callback: CallbackQuery, user: User, session) -> None:
    """List seller's orders."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    seller = user.seller_profile
    
    stmt = (
        select(Order)
        .where(Order.seller_id == seller.id)
        .order_by(Order.created_at.desc())
        .limit(20)
        .options(selectinload(Order.user))
    )
    result = await session.execute(stmt)
    orders = result.scalars().all()
    
    if not orders:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:dashboard")],
        ])
        
        await callback.message.edit_text(
            "📋 <b>Buyurtmalar</b>\n\n"
            "Sizga hali buyurtmalar kelmagan.",
            reply_markup=keyboard,
        )
        await callback.answer()
        return
    
    # Count by status
    pending = sum(1 for o in orders if o.status == OrderStatus.PENDING)
    confirmed = sum(1 for o in orders if o.status == OrderStatus.CONFIRMED)
    processing = sum(1 for o in orders if o.status == OrderStatus.PROCESSING)
    
    text = (
        f"📋 <b>Buyurtmalar</b>\n\n"
        f"⏳ Yangi: {pending} ta\n"
        f"✅ Tasdiqlangan: {confirmed} ta\n"
        f"📦 Tayyorlanmoqda: {processing} ta\n\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    
    # Show recent orders
    for order in orders[:6]:
        status_emoji = {
            OrderStatus.PENDING: "⏳",
            OrderStatus.CONFIRMED: "✅",
            OrderStatus.PROCESSING: "📦",
            OrderStatus.SHIPPED: "🚚",
            OrderStatus.DELIVERED: "🎉",
            OrderStatus.CANCELLED: "❌",
        }.get(order.status, "📋")
        
        buttons.append([
            InlineKeyboardButton(
                text=f"{status_emoji} #{order.id} - {order.total_amount:,.0f} so'm",
                callback_data=f"seller:order:{order.id}",
            )
        ])
    
    # Filter buttons
    buttons.append([
        InlineKeyboardButton(text="⏳ Yangilar", callback_data="seller:orders:pending"),
        InlineKeyboardButton(text="📦 Jarayonda", callback_data="seller:orders:processing"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:dashboard"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("seller:order:"))
async def view_seller_order(callback: CallbackQuery, user: User, session) -> None:
    """View order details for seller."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    order_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = (
        select(Order)
        .where(Order.id == order_id, Order.seller_id == seller.id)
        .options(selectinload(Order.user), selectinload(Order.items))
    )
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        await callback.answer("❌ Buyurtma topilmadi!", show_alert=True)
        return
    
    buyer = order.user
    
    status_names = {
        OrderStatus.PENDING: "⏳ Yangi",
        OrderStatus.CONFIRMED: "✅ Tasdiqlangan",
        OrderStatus.PROCESSING: "📦 Tayyorlanmoqda",
        OrderStatus.SHIPPED: "🚚 Yetkazilmoqda",
        OrderStatus.DELIVERED: "🎉 Yetkazildi",
        OrderStatus.CANCELLED: "❌ Bekor qilingan",
    }
    
    text = (
        f"📋 <b>Buyurtma #{order.id}</b>\n\n"
        f"📊 Holat: {status_names.get(order.status, order.status.value)}\n"
        f"📅 Sana: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"👤 <b>Xaridor:</b>\n"
        f"├ Ism: {buyer.full_name}\n"
        f"├ Tel: {buyer.phone or 'Noma\\'lum'}\n"
        f"└ Manzil: {order.shipping_address or 'Kiritilmagan'}\n\n"
        f"📦 <b>Mahsulotlar:</b>\n"
    )
    
    for item in order.items:
        text += f"  • {item.product_name} x{item.quantity} = {item.total:,.0f} so'm\n"
    
    text += f"\n💰 <b>Jami: {order.total_amount:,.0f} so'm</b>"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    
    # Action buttons based on status
    if order.status == OrderStatus.PENDING:
        buttons.append([
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"seller:confirm_order:{order.id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"seller:reject_order:{order.id}"),
        ])
    elif order.status == OrderStatus.CONFIRMED:
        buttons.append([
            InlineKeyboardButton(text="📦 Tayyorlash", callback_data=f"seller:process_order:{order.id}"),
        ])
    elif order.status == OrderStatus.PROCESSING:
        buttons.append([
            InlineKeyboardButton(text="🚚 Yetkazishga berish", callback_data=f"seller:ship_order:{order.id}"),
        ])
    
    buttons.append([
        InlineKeyboardButton(text="📞 Xaridor bilan bog'lanish", url=f"tg://user?id={buyer.telegram_id}"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:orders"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("seller:confirm_order:"))
async def confirm_order(callback: CallbackQuery, user: User, session) -> None:
    """Confirm pending order."""
    from sqlalchemy import select
    from app.loader import bot
    
    order_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = select(Order).where(Order.id == order_id, Order.seller_id == seller.id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order or order.status != OrderStatus.PENDING:
        await callback.answer("❌ Bu buyurtmani tasdiqlab bo'lmaydi!", show_alert=True)
        return
    
    order.status = OrderStatus.CONFIRMED
    order.confirmed_at = __import__('datetime').datetime.utcnow()
    await session.commit()
    
    # Notify buyer
    try:
        await bot.send_message(
            chat_id=order.user_id_telegram,
            text=f"✅ <b>Buyurtmangiz tasdiqlandi!</b>\n\n"
                 f"📋 Buyurtma #{order.id}\n"
                 f"💰 Summa: {order.total_amount:,.0f} so'm\n\n"
                 f"Tez orada tayyorlanadi.",
        )
    except Exception:
        pass
    
    # Notify admins
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=f"✅ Buyurtma #{order.id} tasdiqlandi sotuvchi tomonidan.",
            )
        except Exception:
            pass
    
    await callback.answer("✅ Buyurtma tasdiqlandi!")
    await view_seller_order(callback, user, session)


@router.callback_query(F.data.startswith("seller:process_order:"))
async def process_order(callback: CallbackQuery, user: User, session) -> None:
    """Mark order as processing."""
    from sqlalchemy import select
    from app.loader import bot
    
    order_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = select(Order).where(Order.id == order_id, Order.seller_id == seller.id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order or order.status != OrderStatus.CONFIRMED:
        await callback.answer("❌ Holat o'zgartirib bo'lmaydi!", show_alert=True)
        return
    
    order.status = OrderStatus.PROCESSING
    await session.commit()
    
    # Notify buyer
    try:
        await bot.send_message(
            chat_id=order.user_id_telegram,
            text=f"📦 <b>Buyurtmangiz tayyorlanmoqda!</b>\n\n"
                 f"📋 Buyurtma #{order.id}",
        )
    except Exception:
        pass
    
    await callback.answer("📦 Buyurtma tayyorlanmoqda!")
    await view_seller_order(callback, user, session)


@router.callback_query(F.data.startswith("seller:ship_order:"))
async def ship_order(callback: CallbackQuery, user: User, session) -> None:
    """Mark order as shipped."""
    from sqlalchemy import select
    from app.loader import bot
    
    order_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = select(Order).where(Order.id == order_id, Order.seller_id == seller.id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order or order.status != OrderStatus.PROCESSING:
        await callback.answer("❌ Holat o'zgartirib bo'lmaydi!", show_alert=True)
        return
    
    order.status = OrderStatus.SHIPPED
    order.shipped_at = __import__('datetime').datetime.utcnow()
    await session.commit()
    
    # Notify buyer
    try:
        await bot.send_message(
            chat_id=order.user_id_telegram,
            text=f"🚚 <b>Buyurtmangiz yetkazilmoqda!</b>\n\n"
                 f"📋 Buyurtma #{order.id}\n"
                 f"📍 Manzil: {order.shipping_address}",
        )
    except Exception:
        pass
    
    await callback.answer("🚚 Buyurtma yetkazishga berildi!")
    await view_seller_order(callback, user, session)


@router.callback_query(F.data.startswith("seller:reject_order:"))
async def reject_order_confirm(callback: CallbackQuery) -> None:
    """Confirm order rejection."""
    order_id = callback.data.split(":")[2]
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha, rad etish", callback_data=f"seller:do_reject:{order_id}"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data=f"seller:order:{order_id}"),
        ],
    ])
    
    await callback.message.edit_text(
        "⚠️ <b>Buyurtmani rad etishni xohlaysizmi?</b>\n\n"
        "Xaridor bu haqda xabardor qilinadi.",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("seller:do_reject:"))
async def do_reject_order(callback: CallbackQuery, user: User, session) -> None:
    """Reject order."""
    from sqlalchemy import select
    from app.loader import bot
    
    order_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = select(Order).where(Order.id == order_id, Order.seller_id == seller.id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    
    if not order:
        await callback.answer("❌ Buyurtma topilmadi!", show_alert=True)
        return
    
    order.status = OrderStatus.CANCELLED
    order.cancelled_at = __import__('datetime').datetime.utcnow()
    order.cancel_reason = "Sotuvchi tomonidan rad etildi"
    await session.commit()
    
    # Notify buyer
    try:
        await bot.send_message(
            chat_id=order.user_id_telegram,
            text=f"❌ <b>Buyurtmangiz rad etildi</b>\n\n"
                 f"📋 Buyurtma #{order.id}\n\n"
                 f"Afsuski, sotuvchi buyurtmangizni rad etdi.\n"
                 f"Iltimos, boshqa mahsulotlarni ko'ring.",
        )
    except Exception:
        pass
    
    await callback.message.edit_text("❌ Buyurtma rad etildi!")
    await callback.answer()


@router.callback_query(F.data == "seller:orders:pending")
async def filter_pending_orders(callback: CallbackQuery, user: User, session) -> None:
    """Filter pending orders."""
    from sqlalchemy import select
    
    seller = user.seller_profile
    
    stmt = (
        select(Order)
        .where(Order.seller_id == seller.id, Order.status == OrderStatus.PENDING)
        .order_by(Order.created_at.desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    orders = result.scalars().all()
    
    if not orders:
        await callback.answer("Yangi buyurtmalar yo'q!", show_alert=True)
        return
    
    text = f"⏳ <b>Yangi buyurtmalar</b> ({len(orders)} ta)\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for order in orders:
        buttons.append([
            InlineKeyboardButton(
                text=f"⏳ #{order.id} - {order.total_amount:,.0f} so'm",
                callback_data=f"seller:order:{order.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:orders"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
