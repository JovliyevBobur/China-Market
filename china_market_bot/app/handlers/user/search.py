"""
🔍 Search Handler Module

Product search functionality with filters.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.models import Product, Category, User
from app.states.user_states import SearchStates

router = Router(name="search")


@router.message(Command("search"))
@router.message(F.text.in_(["🔍 Qidirish", "🔍 Поиск", "🔍 Search"]))
async def start_search(message: Message, state: FSMContext) -> None:
    """Start product search."""
    await state.set_state(SearchStates.entering_query)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="search:cancel")]
    ])
    
    await message.answer(
        "🔍 <b>Mahsulot qidirish</b>\n\n"
        "Qidiruv so'zini kiriting:\n"
        "<i>Masalan: telefon, kiyim, sumka...</i>",
        reply_markup=keyboard,
    )


@router.message(SearchStates.entering_query)
async def process_search(message: Message, session, state: FSMContext) -> None:
    """Process search query."""
    from sqlalchemy import select, or_, func
    
    query = message.text.strip()
    
    if len(query) < 2:
        await message.answer("❌ Qidiruv so'zi kamida 2 ta belgidan iborat bo'lishi kerak!")
        return
    
    # Search products
    search_term = f"%{query}%"
    stmt = (
        select(Product)
        .where(
            Product.is_active == True,
            Product.is_approved == True,
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
            )
        )
        .order_by(Product.view_count.desc())
        .limit(20)
    )
    
    result = await session.execute(stmt)
    products = result.scalars().all()
    
    await state.update_data(query=query, page=1)
    
    if not products:
        await message.answer(
            f"🔍 <b>'{query}'</b> bo'yicha qidiruv\n\n"
            f"❌ Hech narsa topilmadi.\n\n"
            f"💡 <i>Boshqa so'zlar bilan qidirib ko'ring.</i>",
        )
        await state.clear()
        return
    
    text = f"🔍 <b>'{query}'</b> bo'yicha topildi: {len(products)} ta\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    # Show first 5 products
    buttons = []
    for product in products[:5]:
        price = product.discount_price or product.price
        buttons.append([
            InlineKeyboardButton(
                text=f"{product.name[:30]} - {price:,.0f} so'm",
                callback_data=f"product:view:{product.id}",
            )
        ])
    
    if len(products) > 5:
        buttons.append([
            InlineKeyboardButton(text="📄 Ko'proq ko'rish", callback_data=f"search:more:1")
        ])
    
    buttons.append([
        InlineKeyboardButton(text="🔍 Yangi qidiruv", callback_data="search:new"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await message.answer(text, reply_markup=keyboard)
    await state.clear()


@router.callback_query(F.data == "search:cancel")
async def cancel_search(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel search."""
    await state.clear()
    await callback.message.edit_text("❌ Qidiruv bekor qilindi.")
    await callback.answer()


@router.callback_query(F.data == "search:new")
async def new_search(callback: CallbackQuery, state: FSMContext) -> None:
    """Start new search."""
    await state.set_state(SearchStates.entering_query)
    
    await callback.message.edit_text(
        "🔍 <b>Mahsulot qidirish</b>\n\n"
        "Qidiruv so'zini kiriting:",
    )
    await callback.answer()


@router.message(Command("filter"))
async def show_filters(message: Message, session) -> None:
    """Show search filters."""
    from sqlalchemy import select
    
    # Get categories
    stmt = select(Category).where(Category.is_active == True).order_by(Category.sort_order)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    
    # Price filters
    buttons.append([
        InlineKeyboardButton(text="💰 Narx bo'yicha", callback_data="filter:price")
    ])
    
    # Category filters
    for cat in categories[:8]:
        buttons.append([
            InlineKeyboardButton(
                text=f"{cat.icon or '📦'} {cat.name}",
                callback_data=f"filter:cat:{cat.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await message.answer(
        "🔍 <b>Filterlar</b>\n\n"
        "Qidiruv turini tanlang:",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "filter:price")
async def filter_by_price(callback: CallbackQuery) -> None:
    """Filter by price range."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 100,000 so'mgacha", callback_data="price:0:100000")],
        [InlineKeyboardButton(text="💵 100,000 - 500,000", callback_data="price:100000:500000")],
        [InlineKeyboardButton(text="💵 500,000 - 1,000,000", callback_data="price:500000:1000000")],
        [InlineKeyboardButton(text="💵 1,000,000+", callback_data="price:1000000:0")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="filter:back")],
    ])
    
    await callback.message.edit_text(
        "💰 <b>Narx oralig'ini tanlang:</b>",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("price:"))
async def show_price_filtered(callback: CallbackQuery, session) -> None:
    """Show products filtered by price."""
    from sqlalchemy import select, and_
    
    parts = callback.data.split(":")
    min_price = int(parts[1])
    max_price = int(parts[2])
    
    # Build query
    conditions = [Product.is_active == True, Product.is_approved == True]
    
    if min_price > 0:
        conditions.append(Product.price >= min_price)
    if max_price > 0:
        conditions.append(Product.price <= max_price)
    
    stmt = (
        select(Product)
        .where(and_(*conditions))
        .order_by(Product.price.asc())
        .limit(20)
    )
    
    result = await session.execute(stmt)
    products = result.scalars().all()
    
    if not products:
        await callback.answer("❌ Bu narx oralig'ida mahsulot topilmadi!", show_alert=True)
        return
    
    price_text = f"{min_price:,} - {max_price:,}" if max_price > 0 else f"{min_price:,}+"
    text = f"💰 <b>Narx: {price_text} so'm</b>\n\nTopildi: {len(products)} ta\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for product in products[:5]:
        price = product.discount_price or product.price
        buttons.append([
            InlineKeyboardButton(
                text=f"{product.name[:30]} - {price:,.0f} so'm",
                callback_data=f"product:view:{product.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="filter:price")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("filter:cat:"))
async def filter_by_category(callback: CallbackQuery, session) -> None:
    """Filter by category."""
    from sqlalchemy import select
    
    cat_id = int(callback.data.split(":")[2])
    
    # Get category
    stmt = select(Category).where(Category.id == cat_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    
    if not category:
        await callback.answer("❌ Kategoriya topilmadi!", show_alert=True)
        return
    
    # Get products in category
    stmt = (
        select(Product)
        .where(
            Product.category_id == cat_id,
            Product.is_active == True,
            Product.is_approved == True,
        )
        .order_by(Product.sold_count.desc())
        .limit(20)
    )
    
    result = await session.execute(stmt)
    products = result.scalars().all()
    
    if not products:
        await callback.answer("❌ Bu kategoriyada mahsulot topilmadi!", show_alert=True)
        return
    
    text = f"{category.icon or '📦'} <b>{category.name}</b>\n\nTopildi: {len(products)} ta\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for product in products[:5]:
        price = product.discount_price or product.price
        buttons.append([
            InlineKeyboardButton(
                text=f"{product.name[:30]} - {price:,.0f} so'm",
                callback_data=f"product:view:{product.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="filter:back")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "filter:back")
async def back_to_filters(callback: CallbackQuery, session) -> None:
    """Go back to filters."""
    from sqlalchemy import select
    
    # Get categories
    stmt = select(Category).where(Category.is_active == True).order_by(Category.sort_order)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    buttons.append([
        InlineKeyboardButton(text="💰 Narx bo'yicha", callback_data="filter:price")
    ])
    
    for cat in categories[:8]:
        buttons.append([
            InlineKeyboardButton(
                text=f"{cat.icon or '📦'} {cat.name}",
                callback_data=f"filter:cat:{cat.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        "🔍 <b>Filterlar</b>\n\n"
        "Qidiruv turini tanlang:",
        reply_markup=keyboard,
    )
    await callback.answer()
