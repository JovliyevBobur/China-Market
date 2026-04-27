"""
📂 Admin Categories Handler

Category management for admins.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.models import Category
from app.states.admin_states import AdminStates

router = Router(name="admin_categories")


@router.callback_query(F.data == "admin:categories")
async def list_categories(callback: CallbackQuery, session) -> None:
    """List all categories."""
    from sqlalchemy import select
    
    stmt = select(Category).order_by(Category.sort_order)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    
    text = f"📂 <b>Kategoriyalar</b> ({len(categories)} ta)\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for cat in categories[:12]:
        status = "✅" if cat.is_active else "❌"
        buttons.append([
            InlineKeyboardButton(
                text=f"{status} {cat.icon or '📦'} {cat.name}",
                callback_data=f"admin:cat:{cat.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="➕ Yangi kategoriya", callback_data="admin:add_category"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:panel"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("admin:cat:"))
async def view_category(callback: CallbackQuery, session) -> None:
    """View category details."""
    from sqlalchemy import select, func
    from app.database.models import Product
    
    cat_id = int(callback.data.split(":")[2])
    
    stmt = select(Category).where(Category.id == cat_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    
    if not category:
        await callback.answer("❌ Kategoriya topilmadi!", show_alert=True)
        return
    
    # Count products
    stmt = select(func.count(Product.id)).where(Product.category_id == cat_id)
    result = await session.execute(stmt)
    product_count = result.scalar() or 0
    
    status = "✅ Faol" if category.is_active else "❌ Nofaol"
    
    text = (
        f"{category.icon or '📦'} <b>{category.name}</b>\n\n"
        f"📝 Tavsif: {category.description or 'Yo\\'q'}\n"
        f"📦 Mahsulotlar: {product_count} ta\n"
        f"📌 Holat: {status}\n"
        f"🔢 Tartib: {category.sort_order}\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"admin:edit_cat:{cat_id}"),
            InlineKeyboardButton(
                text="❌ O'chirish" if category.is_active else "✅ Faollashtirish",
                callback_data=f"admin:toggle_cat:{cat_id}",
            ),
        ],
        [
            InlineKeyboardButton(text="🗑 O'chirib tashlash", callback_data=f"admin:delete_cat:{cat_id}"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:categories"),
        ],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "admin:add_category")
async def add_category_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Start adding category."""
    await state.set_state(AdminStates.category_name)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:categories")],
    ])
    
    await callback.message.edit_text(
        "📂 <b>Yangi kategoriya</b>\n\n"
        "Kategoriya nomini kiriting:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(AdminStates.category_name)
async def process_category_name(message: Message, state: FSMContext) -> None:
    """Process category name."""
    name = message.text.strip()
    
    if len(name) < 2 or len(name) > 100:
        await message.answer("❌ Nom 2-100 belgi orasida bo'lishi kerak!")
        return
    
    await state.update_data(name=name)
    await state.set_state(AdminStates.category_icon)
    
    await message.answer(
        "📂 <b>Kategoriya ikonkasi</b>\n\n"
        "Emoji kiriting (yoki /skip):\n"
        "Masalan: 📱, 👕, 🍎, 🏠",
    )


@router.message(AdminStates.category_icon)
async def process_category_icon(message: Message, session, state: FSMContext) -> None:
    """Process category icon and save."""
    import re
    
    data = await state.get_data()
    icon = None if message.text == "/skip" else message.text.strip()[:5]
    
    # Generate slug
    slug = re.sub(r'[^\w\s-]', '', data['name'].lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    
    # Create category
    category = Category(
        name=data['name'],
        slug=slug,
        icon=icon,
        is_active=True,
        sort_order=0,
    )
    
    session.add(category)
    await session.commit()
    
    await state.clear()
    
    from app.keyboards.reply.main_menu import create_main_menu
    
    await message.answer(
        f"✅ Kategoriya '{data['name']}' qo'shildi!",
        reply_markup=create_main_menu(),
    )


@router.callback_query(F.data.startswith("admin:toggle_cat:"))
async def toggle_category(callback: CallbackQuery, session) -> None:
    """Toggle category active status."""
    from sqlalchemy import select
    
    cat_id = int(callback.data.split(":")[2])
    
    stmt = select(Category).where(Category.id == cat_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    
    if not category:
        await callback.answer("❌ Kategoriya topilmadi!", show_alert=True)
        return
    
    category.is_active = not category.is_active
    await session.commit()
    
    status = "faollashtirildi ✅" if category.is_active else "o'chirildi ❌"
    await callback.answer(f"Kategoriya {status}")
    await view_category(callback, session)


@router.callback_query(F.data.startswith("admin:delete_cat:"))
async def delete_category_confirm(callback: CallbackQuery) -> None:
    """Confirm category deletion."""
    cat_id = callback.data.split(":")[2]
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"admin:do_delete_cat:{cat_id}"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data=f"admin:cat:{cat_id}"),
        ],
    ])
    
    await callback.message.edit_text(
        "⚠️ <b>Kategoriyani o'chirishni xohlaysizmi?</b>\n\n"
        "Undagi mahsulotlar ham kategoriyasiz qoladi!",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:do_delete_cat:"))
async def delete_category(callback: CallbackQuery, session) -> None:
    """Delete category."""
    from sqlalchemy import select
    
    cat_id = int(callback.data.split(":")[2])
    
    stmt = select(Category).where(Category.id == cat_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    
    if not category:
        await callback.answer("❌ Kategoriya topilmadi!", show_alert=True)
        return
    
    await session.delete(category)
    await session.commit()
    
    await callback.message.edit_text("✅ Kategoriya o'chirildi!")
    await callback.answer()
