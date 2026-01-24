"""
🛒 Cart Handler Module

Handles cart management.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.callbacks import CartCallback, CartItemCallback
from app.config.constants import ErrorMessages, SuccessMessages
from app.database.repositories import CartRepository
from app.keyboards.inline.cart_kb import (
    get_cart_keyboard,
    get_cart_item_keyboard,
    get_empty_cart_keyboard,
)

router = Router(name="cart")


@router.message(F.text.in_(["🛒 Savat", "🛒 Корзина", "🛒 Cart"]))
async def show_cart(
    message: Message,
    session: AsyncSession,
    user=None,
):
    """
    Show user's cart.
    
    Args:
        message: Telegram message
        session: Database session
        user: User model
    """
    if not user:
        await message.answer("Iltimos, avval /start buyrug'ini yuboring.")
        return
    
    cart_repo = CartRepository(session)
    cart = await cart_repo.get_user_cart(user.id)
    
    if cart.is_empty:
        await message.answer(
            "🛒 Savatingiz bo'sh!\n\n"
            "Mahsulotlarni katalogdan qo'shishingiz mumkin.",
            reply_markup=get_empty_cart_keyboard(),
        )
        return
    
    # Format cart message
    text = "🛒 <b>Sizning savatingiz:</b>\n\n"
    
    for i, item in enumerate(cart.items, 1):
        price = f"{item.total_price:,.0f}".replace(",", " ")
        text += f"{i}. {item.product.name[:30]}...\n"
        text += f"   📦 {item.quantity} x {item.product.current_price:,.0f} = {price} so'm\n\n"
    
    total = f"{cart.total:,.0f}".replace(",", " ")
    text += f"💰 <b>Jami:</b> {total} so'm"
    
    await message.answer(
        text,
        reply_markup=get_cart_keyboard(cart.items, cart.total),
        parse_mode="HTML",
    )


@router.callback_query(CartCallback.filter(F.action == "view"))
async def view_cart(
    callback: CallbackQuery,
    session: AsyncSession,
    user=None,
):
    """
    View cart via callback.
    
    Args:
        callback: Callback query
        session: Database session
        user: User model
    """
    if not user:
        await callback.answer("Xatolik yuz berdi!")
        return
    
    cart_repo = CartRepository(session)
    cart = await cart_repo.get_user_cart(user.id)
    
    if cart.is_empty:
        await callback.message.edit_text(
            "🛒 Savatingiz bo'sh!",
            reply_markup=get_empty_cart_keyboard(),
        )
        await callback.answer()
        return
    
    # Format cart message
    text = "🛒 <b>Sizning savatingiz:</b>\n\n"
    
    for i, item in enumerate(cart.items, 1):
        price = f"{item.total_price:,.0f}".replace(",", " ")
        text += f"{i}. {item.product.name[:30]}...\n"
        text += f"   📦 {item.quantity} x {item.product.current_price:,.0f} = {price} so'm\n\n"
    
    total = f"{cart.total:,.0f}".replace(",", " ")
    text += f"💰 <b>Jami:</b> {total} so'm"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_cart_keyboard(cart.items, cart.total),
        parse_mode="HTML",
    )
    
    await callback.answer()


@router.callback_query(CartCallback.filter(F.action == "add"))
async def add_to_cart(
    callback: CallbackQuery,
    callback_data: CartCallback,
    session: AsyncSession,
    user=None,
):
    """
    Add product to cart.
    
    Args:
        callback: Callback query
        callback_data: Cart callback data
        session: Database session
        user: User model
    """
    if not user:
        await callback.answer("Iltimos, avval /start buyrug'ini yuboring!", show_alert=True)
        return
    
    cart_repo = CartRepository(session)
    
    try:
        await cart_repo.add_to_cart(
            user_id=user.id,
            product_id=callback_data.product_id,
            quantity=callback_data.quantity,
        )
        
        await callback.answer(SuccessMessages.ADDED_TO_CART, show_alert=True)
        
    except ValueError as e:
        await callback.answer(str(e), show_alert=True)


@router.callback_query(CartItemCallback.filter(F.action == "remove"))
async def remove_from_cart(
    callback: CallbackQuery,
    callback_data: CartItemCallback,
    session: AsyncSession,
    user=None,
):
    """
    Remove item from cart.
    
    Args:
        callback: Callback query
        callback_data: Cart item callback data
        session: Database session
        user: User model
    """
    if not user:
        await callback.answer("Xatolik yuz berdi!")
        return
    
    cart_repo = CartRepository(session)
    
    # Get cart item to find product_id
    from app.database.models import CartItem
    cart_item = await session.get(CartItem, callback_data.item_id)
    
    if cart_item:
        await cart_repo.remove_from_cart(user.id, cart_item.product_id)
        await callback.answer(SuccessMessages.REMOVED_FROM_CART)
        
        # Refresh cart view
        cart = await cart_repo.get_user_cart(user.id)
        
        if cart.is_empty:
            await callback.message.edit_text(
                "🛒 Savatingiz bo'sh!",
                reply_markup=get_empty_cart_keyboard(),
            )
        else:
            text = "🛒 <b>Sizning savatingiz:</b>\n\n"
            for i, item in enumerate(cart.items, 1):
                price = f"{item.total_price:,.0f}".replace(",", " ")
                text += f"{i}. {item.product.name[:30]}...\n"
                text += f"   📦 {item.quantity} x {item.product.current_price:,.0f} = {price} so'm\n\n"
            
            total = f"{cart.total:,.0f}".replace(",", " ")
            text += f"💰 <b>Jami:</b> {total} so'm"
            
            await callback.message.edit_text(
                text,
                reply_markup=get_cart_keyboard(cart.items, cart.total),
                parse_mode="HTML",
            )
    else:
        await callback.answer("Element topilmadi!")


@router.callback_query(CartCallback.filter(F.action == "clear"))
async def clear_cart(
    callback: CallbackQuery,
    session: AsyncSession,
    user=None,
):
    """
    Clear all cart items.
    
    Args:
        callback: Callback query
        session: Database session
        user: User model
    """
    if not user:
        await callback.answer("Xatolik yuz berdi!")
        return
    
    cart_repo = CartRepository(session)
    await cart_repo.clear_cart(user.id)
    
    await callback.message.edit_text(
        "🛒 Savatingiz tozalandi!",
        reply_markup=get_empty_cart_keyboard(),
    )
    
    await callback.answer("Savat tozalandi!")


@router.callback_query(CartItemCallback.filter(F.action == "inc"))
async def increase_quantity(
    callback: CallbackQuery,
    callback_data: CartItemCallback,
    session: AsyncSession,
    user=None,
):
    """
    Increase cart item quantity.
    
    Args:
        callback: Callback query
        callback_data: Cart item callback data
        session: Database session
        user: User model
    """
    if not user:
        await callback.answer("Xatolik yuz berdi!")
        return
    
    from app.database.models import CartItem
    cart_item = await session.get(CartItem, callback_data.item_id)
    
    if cart_item:
        cart_repo = CartRepository(session)
        new_qty = cart_item.quantity + 1
        
        if new_qty <= cart_item.product.available_quantity:
            await cart_repo.update_quantity(
                user.id,
                cart_item.product_id,
                new_qty,
            )
            await callback.answer(f"Miqdor: {new_qty}")
        else:
            await callback.answer(ErrorMessages.INSUFFICIENT_STOCK, show_alert=True)


@router.callback_query(CartItemCallback.filter(F.action == "dec"))
async def decrease_quantity(
    callback: CallbackQuery,
    callback_data: CartItemCallback,
    session: AsyncSession,
    user=None,
):
    """
    Decrease cart item quantity.
    
    Args:
        callback: Callback query
        callback_data: Cart item callback data
        session: Database session
        user: User model
    """
    if not user:
        await callback.answer("Xatolik yuz berdi!")
        return
    
    from app.database.models import CartItem
    cart_item = await session.get(CartItem, callback_data.item_id)
    
    if cart_item:
        cart_repo = CartRepository(session)
        new_qty = cart_item.quantity - 1
        
        if new_qty >= 1:
            await cart_repo.update_quantity(
                user.id,
                cart_item.product_id,
                new_qty,
            )
            await callback.answer(f"Miqdor: {new_qty}")
        else:
            await callback.answer("Minimal miqdor: 1")
