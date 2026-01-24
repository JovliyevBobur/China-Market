"""
🛍️ Catalog Handler Module

Handles catalog browsing and product viewing.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.callbacks import CatalogCallback, CategoryCallback, ProductCallback
from app.config.constants import PRODUCTS_PER_PAGE
from app.database.repositories import ProductRepository
from app.keyboards.inline.catalog_kb import (
    get_categories_keyboard,
    get_products_keyboard,
    get_product_keyboard,
)
from app.states import UserStates

router = Router(name="catalog")


@router.message(F.text.in_(["🛍️ Katalog", "🛍️ Каталог", "🛍️ Catalog"]))
async def show_catalog(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    """
    Show main catalog with categories.
    
    Args:
        message: Telegram message
        state: FSM state
        session: Database session
    """
    from app.database.models import Category
    from sqlalchemy import select
    
    # Get root categories
    result = await session.execute(
        select(Category)
        .where(
            Category.parent_id.is_(None),
            Category.is_active == True,
        )
        .order_by(Category.sort_order)
    )
    categories = result.scalars().all()
    
    await message.answer(
        "📁 <b>Kategoriyalarni tanlang:</b>",
        reply_markup=get_categories_keyboard(categories),
        parse_mode="HTML",
    )
    
    await state.set_state(UserStates.browsing_catalog)


@router.callback_query(CategoryCallback.filter(F.action == "select"))
async def select_category(
    callback: CallbackQuery,
    callback_data: CategoryCallback,
    state: FSMContext,
    session: AsyncSession,
):
    """
    Handle category selection.
    
    Args:
        callback: Callback query
        callback_data: Category callback data
        state: FSM state
        session: Database session
    """
    from app.database.models import Category
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    category_id = callback_data.category_id
    
    # Get category with children
    result = await session.execute(
        select(Category)
        .options(selectinload(Category.children))
        .where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        await callback.answer("Kategoriya topilmadi!", show_alert=True)
        return
    
    # If has children, show subcategories
    if category.has_children:
        await callback.message.edit_text(
            f"📁 <b>{category.name}</b>\n\n"
            "Subkategoriyani tanlang:",
            reply_markup=get_categories_keyboard(
                category.children,
                parent_id=category.parent_id,
                show_back=True,
            ),
            parse_mode="HTML",
        )
    else:
        # Show products
        product_repo = ProductRepository(session)
        products = await product_repo.get_by_category(
            category_id=category_id,
            limit=PRODUCTS_PER_PAGE,
        )
        
        from app.database.repositories.product_repo import ProductRepository
        total = await product_repo.count_by_category(category_id)
        total_pages = (total + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE
        
        if not products:
            await callback.message.edit_text(
                f"📁 <b>{category.name}</b>\n\n"
                "Bu kategoriyada mahsulotlar yo'q.",
                reply_markup=get_categories_keyboard([], show_back=True),
                parse_mode="HTML",
            )
            return
        
        await callback.message.edit_text(
            f"📁 <b>{category.name}</b>\n\n"
            f"📦 Mahsulotlar soni: {total}",
            reply_markup=get_products_keyboard(
                products,
                category_id=category_id,
                page=1,
                total_pages=total_pages,
            ),
            parse_mode="HTML",
        )
    
    await callback.answer()


@router.callback_query(ProductCallback.filter(F.action == "view"))
async def view_product(
    callback: CallbackQuery,
    callback_data: ProductCallback,
    state: FSMContext,
    session: AsyncSession,
    user=None,
):
    """
    View product details.
    
    Args:
        callback: Callback query
        callback_data: Product callback data
        state: FSM state
        session: Database session
        user: User model
    """
    product_repo = ProductRepository(session)
    product = await product_repo.get_by_id_with_relations(callback_data.product_id)
    
    if not product:
        await callback.answer("Mahsulot topilmadi!", show_alert=True)
        return
    
    # Increment view count
    await product_repo.increment_view(product.id)
    
    # Check if in cart
    in_cart = False
    if user:
        from app.database.repositories import CartRepository
        cart_repo = CartRepository(session)
        cart_item = await cart_repo.get_cart_item(user.id, product.id)
        in_cart = cart_item is not None
    
    # Format product message
    price = f"{product.current_price:,.0f}".replace(",", " ")
    
    text = (
        f"📦 <b>{product.name}</b>\n\n"
        f"{product.description[:500]}...\n\n"
        f"💰 <b>Narxi:</b> {price} so'm"
    )
    
    if product.has_discount:
        old_price = f"{product.price:,.0f}".replace(",", " ")
        text += f" <s>{old_price}</s>"
    
    text += f"\n📊 <b>Mavjud:</b> {product.available_quantity} dona"
    text += f"\n⭐ <b>Reyting:</b> {product.rating:.1f} ({product.review_count} sharh)"
    
    # Send with image if available
    if product.main_image:
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=product.main_image,
                caption=text,
                reply_markup=get_product_keyboard(
                    product,
                    quantity=1,
                    in_cart=in_cart,
                ),
                parse_mode="HTML",
            )
        except Exception:
            await callback.message.edit_text(
                text,
                reply_markup=get_product_keyboard(
                    product,
                    quantity=1,
                    in_cart=in_cart,
                ),
                parse_mode="HTML",
            )
    else:
        await callback.message.edit_text(
            text,
            reply_markup=get_product_keyboard(
                product,
                quantity=1,
                in_cart=in_cart,
            ),
            parse_mode="HTML",
        )
    
    await state.set_state(UserStates.viewing_product)
    await state.update_data(product_id=product.id)
    await callback.answer()


@router.callback_query(CatalogCallback.filter(F.action == "view"))
async def paginate_products(
    callback: CallbackQuery,
    callback_data: CatalogCallback,
    session: AsyncSession,
):
    """
    Handle product pagination.
    
    Args:
        callback: Callback query
        callback_data: Catalog callback data
        session: Database session
    """
    product_repo = ProductRepository(session)
    
    page = callback_data.page
    category_id = callback_data.category_id
    offset = (page - 1) * PRODUCTS_PER_PAGE
    
    products = await product_repo.get_by_category(
        category_id=category_id,
        limit=PRODUCTS_PER_PAGE,
        offset=offset,
    )
    
    total = await product_repo.count_by_category(category_id)
    total_pages = (total + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE
    
    await callback.message.edit_reply_markup(
        reply_markup=get_products_keyboard(
            products,
            category_id=category_id,
            page=page,
            total_pages=total_pages,
        ),
    )
    
    await callback.answer()
