"""
🏪 Seller Dashboard Handler

Main seller panel with statistics and quick actions.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.database.models import User, Seller, Product, Order
from app.filters.seller import SellerFilter

router = Router(name="seller_dashboard")
router.message.filter(SellerFilter())
router.callback_query.filter(SellerFilter())


@router.message(Command("seller"))
@router.message(F.text.in_(["🏪 Sotuvchi paneli", "🏪 Панель продавца", "🏪 Seller Panel"]))
async def seller_dashboard(message: Message, user: User, session) -> None:
    """Show seller dashboard."""
    from sqlalchemy import select, func
    from sqlalchemy.orm import selectinload
    
    # Check if user is seller
    if not user.seller_profile:
        # Offer to become seller
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Sotuvchi bo'lish", callback_data="seller:register")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
        ])
        
        await message.answer(
            "🏪 <b>Sotuvchi paneli</b>\n\n"
            "Siz hali sotuvchi emassiz.\n"
            "Sotuvchi bo'lish uchun ro'yxatdan o'ting!",
            reply_markup=keyboard,
        )
        return
    
    seller = user.seller_profile
    
    # Get statistics
    # Total products
    stmt = select(func.count(Product.id)).where(Product.seller_id == seller.id)
    result = await session.execute(stmt)
    total_products = result.scalar() or 0
    
    # Active products
    stmt = select(func.count(Product.id)).where(
        Product.seller_id == seller.id,
        Product.is_active == True,
        Product.is_approved == True,
    )
    result = await session.execute(stmt)
    active_products = result.scalar() or 0
    
    # Pending orders
    from app.config.constants import OrderStatus
    stmt = select(func.count(Order.id)).where(
        Order.seller_id == seller.id,
        Order.status.in_([OrderStatus.PENDING, OrderStatus.CONFIRMED]),
    )
    result = await session.execute(stmt)
    pending_orders = result.scalar() or 0
    
    # Total sales
    stmt = select(func.sum(Order.total_amount)).where(
        Order.seller_id == seller.id,
        Order.status == OrderStatus.DELIVERED,
    )
    result = await session.execute(stmt)
    total_sales = result.scalar() or 0
    
    # Balance
    balance = seller.balance or 0
    
    status_text = "✅ Tasdiqlangan" if seller.is_verified else "⏳ Kutilmoqda"
    
    text = (
        f"🏪 <b>Sotuvchi paneli</b>\n\n"
        f"👋 Xush kelibsiz, {user.full_name}!\n\n"
        f"📊 <b>Statistika:</b>\n"
        f"├ 📦 Mahsulotlar: {total_products} ta ({active_products} faol)\n"
        f"├ 📋 Kutilayotgan buyurtmalar: {pending_orders} ta\n"
        f"├ 💰 Jami sotuvlar: {total_sales:,.0f} so'm\n"
        f"└ 💳 Balans: {balance:,.0f} so'm\n\n"
        f"📌 Holat: {status_text}\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📦 Mahsulotlarim", callback_data="seller:products"),
            InlineKeyboardButton(text="➕ Yangi mahsulot", callback_data="seller:add_product"),
        ],
        [
            InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="seller:orders"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="seller:analytics"),
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="seller:settings"),
            InlineKeyboardButton(text="💳 Balans", callback_data="seller:balance"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="menu:main"),
        ],
    ])
    
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "seller:register")
async def register_seller(callback: CallbackQuery, user: User, session) -> None:
    """Start seller registration."""
    from app.states.seller_states import SellerRegistrationStates
    from aiogram.fsm.context import FSMContext
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Ro'yxatdan o'tish", callback_data="seller:reg_start")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
    ])
    
    await callback.message.edit_text(
        "🏪 <b>Sotuvchi bo'lish</b>\n\n"
        "Sotuvchi sifatida ro'yxatdan o'tish uchun quyidagi ma'lumotlar kerak:\n\n"
        "1️⃣ Do'kon nomi\n"
        "2️⃣ Telefon raqam\n"
        "3️⃣ Manzil\n"
        "4️⃣ Tavsif\n\n"
        "Davom etasizmi?",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "seller:reg_start")
async def start_seller_registration(callback: CallbackQuery, state) -> None:
    """Start registration process."""
    from app.states.seller_states import SellerRegistrationStates
    
    await state.set_state(SellerRegistrationStates.entering_company_name)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="seller:cancel_reg")],
    ])
    
    await callback.message.edit_text(
        "1️⃣ <b>Do'kon nomini kiriting:</b>\n\n"
        "<i>Masalan: Ali Electronics, Malika Tekstil...</i>",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "seller:cancel_reg")
async def cancel_registration(callback: CallbackQuery, state) -> None:
    """Cancel seller registration."""
    await state.clear()
    
    await callback.message.edit_text(
        "❌ Ro'yxatdan o'tish bekor qilindi.",
    )
    await callback.answer()


@router.callback_query(F.data == "seller:dashboard")
async def dashboard_callback(callback: CallbackQuery, user: User, session) -> None:
    """Show seller dashboard (callback version)."""
    from sqlalchemy import select, func
    
    seller = user.seller_profile
    if not seller:
        await callback.answer("❌ Siz sotuvchi emassiz!", show_alert=True)
        return
    
    # Get statistics
    stmt = select(func.count(Product.id)).where(Product.seller_id == seller.id)
    result = await session.execute(stmt)
    total_products = result.scalar() or 0
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📦 Mahsulotlarim", callback_data="seller:products"),
            InlineKeyboardButton(text="➕ Yangi", callback_data="seller:add_product"),
        ],
        [
            InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="seller:orders"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="seller:analytics"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="menu:main"),
        ],
    ])
    
    await callback.message.edit_text(
        f"🏪 <b>Sotuvchi paneli</b>\n\n"
        f"📦 Mahsulotlar: {total_products} ta\n"
        f"💳 Balans: {seller.balance:,.0f} so'm",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "seller:balance")
async def show_balance(callback: CallbackQuery, user: User) -> None:
    """Show seller balance."""
    seller = user.seller_profile
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Pul yechish", callback_data="seller:withdraw")],
        [InlineKeyboardButton(text="📜 Tranzaksiyalar tarixi", callback_data="seller:transactions")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:dashboard")],
    ])
    
    await callback.message.edit_text(
        f"💰 <b>Balans</b>\n\n"
        f"💳 Joriy balans: <b>{seller.balance:,.0f} so'm</b>\n"
        f"📈 Jami daromad: {seller.total_earnings:,.0f} so'm\n\n"
        f"<i>Minimal yechish summasi: 100,000 so'm</i>",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "seller:settings")
async def show_settings(callback: CallbackQuery, user: User) -> None:
    """Show seller settings."""
    seller = user.seller_profile
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Do'kon nomini o'zgartirish", callback_data="seller:edit_name")],
        [InlineKeyboardButton(text="📱 Telefon", callback_data="seller:edit_phone")],
        [InlineKeyboardButton(text="📝 Tavsif", callback_data="seller:edit_desc")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:dashboard")],
    ])
    
    await callback.message.edit_text(
        f"⚙️ <b>Do'kon sozlamalari</b>\n\n"
        f"🏪 Nom: {seller.company_name}\n"
        f"📱 Telefon: {seller.phone or 'Kiritilmagan'}\n"
        f"📝 Tavsif: {seller.description[:100] if seller.description else 'Yo\\'q'}...",
        reply_markup=keyboard,
    )
    await callback.answer()
