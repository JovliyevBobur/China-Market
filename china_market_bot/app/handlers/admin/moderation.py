"""
🔍 Admin Moderation Handler

Product moderation for admins.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.config import settings
from app.database.models import Product
from app.config.constants import ModerationStatus

router = Router(name="admin_moderation")


@router.callback_query(F.data == "admin:moderation")
async def moderation_queue(callback: CallbackQuery, session) -> None:
    """Show moderation queue."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    stmt = (
        select(Product)
        .where(Product.is_approved == False)
        .order_by(Product.created_at)
        .limit(15)
        .options(selectinload(Product.seller))
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    
    if not products:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:panel")],
        ])
        
        await callback.message.edit_text(
            "🔍 <b>Moderatsiya</b>\n\n"
            "✅ Barcha mahsulotlar tekshirilgan.\n"
            "Hozircha moderatsiya navbati bo'sh.",
            reply_markup=keyboard,
        )
        await callback.answer()
        return
    
    text = f"🔍 <b>Moderatsiya navbati</b> ({len(products)} ta)\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for product in products[:10]:
        seller_name = product.seller.company_name[:15] if product.seller else "Noma'lum"
        buttons.append([
            InlineKeyboardButton(
                text=f"⏳ {product.name[:25]} ({seller_name})",
                callback_data=f"admin:moderate:{product.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:panel"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("admin:moderate:"))
async def moderate_product(callback: CallbackQuery, session) -> None:
    """Moderate single product."""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    product_id = int(callback.data.split(":")[2])
    
    stmt = (
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.seller), selectinload(Product.category))
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    
    if not product:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return
    
    seller_name = product.seller.company_name if product.seller else "Noma'lum"
    category_name = product.category.name if product.category else "Kategoriyasiz"
    
    text = (
        f"📦 <b>Moderatsiya</b>\n\n"
        f"📝 <b>{product.name}</b>\n\n"
        f"📝 Tavsif:\n{product.description[:300]}...\n\n"
        f"💰 Narx: {product.price:,.0f} so'm\n"
        f"📦 Miqdor: {product.quantity} ta\n"
        f"📂 Kategoriya: {category_name}\n"
        f"🏪 Sotuvchi: {seller_name}\n"
        f"📅 Qo'shilgan: {product.created_at.strftime('%d.%m.%Y %H:%M')}\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"admin:approve_product:{product.id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"admin:reject_product:{product.id}"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:moderation"),
        ],
    ])
    
    # Send with photo if available
    if product.images:
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=product.images[0],
                caption=text,
                reply_markup=keyboard,
            )
        except Exception:
            await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text, reply_markup=keyboard)
    
    await callback.answer()


@router.callback_query(F.data.startswith("admin:approve_product:"))
async def approve_product(callback: CallbackQuery, session) -> None:
    """Approve product."""
    from sqlalchemy import select
    from app.loader import bot
    
    product_id = int(callback.data.split(":")[2])
    
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    
    if not product:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return
    
    product.is_approved = True
    product.moderation_status = ModerationStatus.APPROVED
    await session.commit()
    
    # Notify seller
    if product.seller:
        try:
            await bot.send_message(
                chat_id=product.seller.user_id_telegram,
                text=f"✅ <b>Mahsulotingiz tasdiqlandi!</b>\n\n"
                     f"📦 {product.name}\n\n"
                     f"Endi u bozorda ko'rinadi.",
            )
        except Exception:
            pass
    
    await callback.answer("✅ Mahsulot tasdiqlandi!")
    
    # Go back to moderation queue
    await moderation_queue(callback, session)


@router.callback_query(F.data.startswith("admin:reject_product:"))
async def reject_product_confirm(callback: CallbackQuery) -> None:
    """Confirm product rejection."""
    product_id = callback.data.split(":")[2]
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚫 Spam/Reklama", callback_data=f"admin:do_reject:{product_id}:spam")],
        [InlineKeyboardButton(text="📝 Noto'g'ri ma'lumot", callback_data=f"admin:do_reject:{product_id}:info")],
        [InlineKeyboardButton(text="🔞 Taqiqlangan mahsulot", callback_data=f"admin:do_reject:{product_id}:banned")],
        [InlineKeyboardButton(text="❓ Boshqa sabab", callback_data=f"admin:do_reject:{product_id}:other")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"admin:moderate:{product_id}")],
    ])
    
    await callback.message.edit_text(
        "❌ <b>Rad etish sababi:</b>\n\n"
        "Quyidagilardan birini tanlang:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:do_reject:"))
async def do_reject_product(callback: CallbackQuery, session) -> None:
    """Reject product."""
    from sqlalchemy import select
    from app.loader import bot
    
    parts = callback.data.split(":")
    product_id = int(parts[2])
    reason_code = parts[3]
    
    reasons = {
        "spam": "Spam yoki reklama",
        "info": "Noto'g'ri ma'lumotlar",
        "banned": "Taqiqlangan mahsulot",
        "other": "Qoidalarga mos emas",
    }
    reason = reasons.get(reason_code, "Noma'lum sabab")
    
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    
    if not product:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return
    
    product.moderation_status = ModerationStatus.REJECTED
    product.is_active = False
    await session.commit()
    
    # Notify seller
    if product.seller:
        try:
            await bot.send_message(
                chat_id=product.seller.user_id_telegram,
                text=f"❌ <b>Mahsulotingiz rad etildi</b>\n\n"
                     f"📦 {product.name}\n\n"
                     f"Sabab: {reason}\n\n"
                     f"Iltimos, mahsulotni tahrirlang va qayta yuboring.",
            )
        except Exception:
            pass
    
    await callback.answer("❌ Mahsulot rad etildi!")
    
    # Go back to moderation queue
    await moderation_queue(callback, session)
