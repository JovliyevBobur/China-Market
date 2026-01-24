"""
📦 Seller Products Handler

Product management for sellers - add, edit, delete products.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.database.models import User, Seller, Product, Category
from app.filters.seller import SellerFilter
from app.states.seller_states import ProductStates

router = Router(name="seller_products")
router.message.filter(SellerFilter())
router.callback_query.filter(SellerFilter())


@router.callback_query(F.data == "seller:products")
async def list_products(callback: CallbackQuery, user: User, session) -> None:
    """List seller's products."""
    from sqlalchemy import select
    
    seller = user.seller_profile
    
    stmt = (
        select(Product)
        .where(Product.seller_id == seller.id)
        .order_by(Product.created_at.desc())
        .limit(20)
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    
    if not products:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Mahsulot qo'shish", callback_data="seller:add_product")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:dashboard")],
        ])
        
        await callback.message.edit_text(
            "📦 <b>Mahsulotlarim</b>\n\n"
            "Sizda hali mahsulotlar yo'q.\n"
            "Birinchi mahsulotni qo'shing!",
            reply_markup=keyboard,
        )
        await callback.answer()
        return
    
    text = f"📦 <b>Mahsulotlarim</b> ({len(products)} ta)\n\n"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for product in products[:8]:
        status = "✅" if product.is_active and product.is_approved else "⏳" if not product.is_approved else "❌"
        buttons.append([
            InlineKeyboardButton(
                text=f"{status} {product.name[:25]} - {product.price:,.0f} so'm",
                callback_data=f"seller:product:{product.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="➕ Yangi mahsulot", callback_data="seller:add_product"),
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:dashboard"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("seller:product:"))
async def view_product(callback: CallbackQuery, user: User, session) -> None:
    """View product details for seller."""
    from sqlalchemy import select
    
    product_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = select(Product).where(Product.id == product_id, Product.seller_id == seller.id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    
    if not product:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return
    
    status = "✅ Faol" if product.is_active else "❌ Nofaol"
    moderation = "✅ Tasdiqlangan" if product.is_approved else "⏳ Moderatsiyada"
    
    text = (
        f"📦 <b>{product.name}</b>\n\n"
        f"💰 Narx: {product.price:,.0f} so'm\n"
        f"{'💸 Chegirma: ' + str(int(product.discount_price)) + ' so\\m' if product.discount_price else ''}\n"
        f"📦 Omborda: {product.quantity} ta\n"
        f"👁 Ko'rishlar: {product.view_count}\n"
        f"🛒 Sotilgan: {product.sold_count}\n\n"
        f"📌 Holat: {status}\n"
        f"🔍 Moderatsiya: {moderation}\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"seller:edit_product:{product.id}"),
            InlineKeyboardButton(
                text="❌ O'chirish" if product.is_active else "✅ Faollashtirish",
                callback_data=f"seller:toggle_product:{product.id}",
            ),
        ],
        [
            InlineKeyboardButton(text="💰 Narxni o'zgartirish", callback_data=f"seller:price_product:{product.id}"),
            InlineKeyboardButton(text="📦 Miqdor", callback_data=f"seller:qty_product:{product.id}"),
        ],
        [
            InlineKeyboardButton(text="🗑 O'chirib tashlash", callback_data=f"seller:delete_product:{product.id}"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:products"),
        ],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "seller:add_product")
async def start_add_product(callback: CallbackQuery, state: FSMContext, session) -> None:
    """Start adding new product."""
    from sqlalchemy import select
    
    # Get categories
    stmt = select(Category).where(Category.is_active == True).order_by(Category.sort_order)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    
    if not categories:
        await callback.answer("❌ Kategoriyalar mavjud emas!", show_alert=True)
        return
    
    await state.set_state(ProductStates.selecting_category)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    buttons = []
    for cat in categories[:12]:
        buttons.append([
            InlineKeyboardButton(
                text=f"{cat.icon or '📦'} {cat.name}",
                callback_data=f"add_cat:{cat.id}",
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="seller:cancel_add"),
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        "➕ <b>Yangi mahsulot qo'shish</b>\n\n"
        "1️⃣ Kategoriyani tanlang:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("add_cat:"), ProductStates.selecting_category)
async def select_category(callback: CallbackQuery, state: FSMContext) -> None:
    """Select category for new product."""
    cat_id = int(callback.data.split(":")[1])
    
    await state.update_data(category_id=cat_id)
    await state.set_state(ProductStates.entering_name)
    
    await callback.message.edit_text(
        "2️⃣ <b>Mahsulot nomini kiriting:</b>\n\n"
        "<i>Masalan: iPhone 15 Pro Max 256GB</i>\n\n"
        "/cancel - bekor qilish",
    )
    await callback.answer()


@router.message(ProductStates.entering_name)
async def enter_product_name(message: Message, state: FSMContext) -> None:
    """Enter product name."""
    name = message.text.strip()
    
    if len(name) < 3 or len(name) > 200:
        await message.answer("❌ Nom 3-200 belgi orasida bo'lishi kerak!")
        return
    
    await state.update_data(name=name)
    await state.set_state(ProductStates.entering_description)
    
    await message.answer(
        "3️⃣ <b>Mahsulot tavsifini kiriting:</b>\n\n"
        "<i>Mahsulot haqida batafsil ma'lumot yozing (kamida 20 belgi)</i>\n\n"
        "/cancel - bekor qilish",
    )


@router.message(ProductStates.entering_description)
async def enter_product_description(message: Message, state: FSMContext) -> None:
    """Enter product description."""
    desc = message.text.strip()
    
    if len(desc) < 20:
        await message.answer("❌ Tavsif kamida 20 belgi bo'lishi kerak!")
        return
    
    await state.update_data(description=desc)
    await state.set_state(ProductStates.entering_price)
    
    await message.answer(
        "4️⃣ <b>Narxni kiriting (so'mda):</b>\n\n"
        "<i>Masalan: 1500000</i>\n\n"
        "/cancel - bekor qilish",
    )


@router.message(ProductStates.entering_price)
async def enter_product_price(message: Message, state: FSMContext) -> None:
    """Enter product price."""
    try:
        price = int(message.text.strip().replace(" ", "").replace(",", ""))
        if price < 1000 or price > 100_000_000:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri narx! 1,000 - 100,000,000 so'm orasida bo'lishi kerak.")
        return
    
    await state.update_data(price=price)
    await state.set_state(ProductStates.entering_quantity)
    
    await message.answer(
        "5️⃣ <b>Ombordagi miqdorni kiriting:</b>\n\n"
        "<i>Masalan: 10</i>\n\n"
        "/cancel - bekor qilish",
    )


@router.message(ProductStates.entering_quantity)
async def enter_product_quantity(message: Message, state: FSMContext) -> None:
    """Enter product quantity."""
    try:
        qty = int(message.text.strip())
        if qty < 1 or qty > 10000:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Noto'g'ri miqdor! 1 - 10,000 orasida bo'lishi kerak.")
        return
    
    await state.update_data(quantity=qty)
    await state.set_state(ProductStates.uploading_images)
    
    await message.answer(
        "6️⃣ <b>Mahsulot rasmini yuboring:</b>\n\n"
        "<i>Rasm yuboring yoki /skip bilan o'tkazib yuboring</i>\n\n"
        "/cancel - bekor qilish\n"
        "/skip - rasmisiz davom etish",
    )


@router.message(ProductStates.uploading_images, F.photo)
async def upload_product_image(message: Message, state: FSMContext) -> None:
    """Upload product image."""
    photo = message.photo[-1]  # Get largest size
    file_id = photo.file_id
    
    await state.update_data(image=file_id)
    await state.set_state(ProductStates.confirming)
    
    # Get data to show confirmation
    data = await state.get_data()
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="seller:confirm_product"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="seller:cancel_add"),
        ],
    ])
    
    await message.answer(
        f"📦 <b>Mahsulot ma'lumotlari:</b>\n\n"
        f"📝 Nom: {data['name']}\n"
        f"💰 Narx: {data['price']:,} so'm\n"
        f"📦 Miqdor: {data['quantity']} ta\n\n"
        f"Tasdiqlaysizmi?",
        reply_markup=keyboard,
    )


@router.message(ProductStates.uploading_images, F.text == "/skip")
async def skip_image(message: Message, state: FSMContext) -> None:
    """Skip image upload."""
    await state.update_data(image=None)
    await state.set_state(ProductStates.confirming)
    
    data = await state.get_data()
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="seller:confirm_product"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="seller:cancel_add"),
        ],
    ])
    
    await message.answer(
        f"📦 <b>Mahsulot ma'lumotlari:</b>\n\n"
        f"📝 Nom: {data['name']}\n"
        f"💰 Narx: {data['price']:,} so'm\n"
        f"📦 Miqdor: {data['quantity']} ta\n\n"
        f"Tasdiqlaysizmi?",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "seller:confirm_product")
async def confirm_add_product(callback: CallbackQuery, user: User, session, state: FSMContext) -> None:
    """Confirm and save new product."""
    from app.loader import bot
    import re
    
    data = await state.get_data()
    seller = user.seller_profile
    
    # Generate slug
    slug = re.sub(r'[^\w\s-]', '', data['name'].lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    slug = f"{slug}-{seller.id}"
    
    # Create product
    product = Product(
        seller_id=seller.id,
        category_id=data['category_id'],
        name=data['name'],
        description=data['description'],
        price=data['price'],
        quantity=data['quantity'],
        slug=slug,
        is_active=True,
        is_approved=False,  # Needs moderation
    )
    
    if data.get('image'):
        product.images = [data['image']]
    
    session.add(product)
    await session.commit()
    await session.refresh(product)
    
    await state.clear()
    
    # Notify admins about new product
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=f"📦 <b>Yangi mahsulot!</b>\n\n"
                     f"🏪 Sotuvchi: {seller.company_name}\n"
                     f"📝 Mahsulot: {product.name}\n"
                     f"💰 Narx: {product.price:,} so'm\n\n"
                     f"Moderatsiya kutilmoqda.",
            )
        except Exception:
            pass
    
    from app.keyboards.reply.main_menu import create_main_menu
    
    await callback.message.edit_text(
        f"✅ <b>Mahsulot qo'shildi!</b>\n\n"
        f"📦 {product.name}\n"
        f"💰 {product.price:,} so'm\n\n"
        f"⏳ Mahsulot moderatsiyadan o'tkaziladi.",
    )
    await callback.answer("✅ Mahsulot saqlandi!")


@router.callback_query(F.data == "seller:cancel_add")
async def cancel_add_product(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel adding product."""
    await state.clear()
    
    await callback.message.edit_text(
        "❌ Mahsulot qo'shish bekor qilindi.",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("seller:toggle_product:"))
async def toggle_product(callback: CallbackQuery, user: User, session) -> None:
    """Toggle product active status."""
    from sqlalchemy import select
    
    product_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = select(Product).where(Product.id == product_id, Product.seller_id == seller.id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    
    if not product:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return
    
    product.is_active = not product.is_active
    await session.commit()
    
    status = "faollashtirildi ✅" if product.is_active else "o'chirildi ❌"
    await callback.answer(f"Mahsulot {status}")
    
    # Redirect back to product view
    await view_product(callback, user, session)


@router.callback_query(F.data.startswith("seller:delete_product:"))
async def delete_product_confirm(callback: CallbackQuery) -> None:
    """Confirm product deletion."""
    product_id = callback.data.split(":")[2]
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"seller:confirm_delete:{product_id}"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data=f"seller:product:{product_id}"),
        ],
    ])
    
    await callback.message.edit_text(
        "⚠️ <b>Mahsulotni o'chirishni xohlaysizmi?</b>\n\n"
        "Bu amalni qaytarib bo'lmaydi!",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("seller:confirm_delete:"))
async def confirm_delete_product(callback: CallbackQuery, user: User, session) -> None:
    """Delete product."""
    from sqlalchemy import select
    
    product_id = int(callback.data.split(":")[2])
    seller = user.seller_profile
    
    stmt = select(Product).where(Product.id == product_id, Product.seller_id == seller.id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    
    if not product:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return
    
    await session.delete(product)
    await session.commit()
    
    await callback.message.edit_text(
        "✅ Mahsulot o'chirildi!",
    )
    await callback.answer()
