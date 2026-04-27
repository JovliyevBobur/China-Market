"""
📊 Seller Analytics Handler

Sales statistics and analytics for sellers.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.config.constants import OrderStatus
from app.database.models import User, Seller, Product, Order
from app.filters.seller import SellerFilter

router = Router(name="seller_analytics")
router.callback_query.filter(SellerFilter())


@router.callback_query(F.data == "seller:analytics")
async def show_analytics(callback: CallbackQuery, user: User, session) -> None:
    """Show seller analytics."""
    from sqlalchemy import select, func
    from datetime import datetime, timedelta
    
    seller = user.seller_profile
    
    # Date ranges
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
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
    
    # Total orders
    stmt = select(func.count(Order.id)).where(Order.seller_id == seller.id)
    result = await session.execute(stmt)
    total_orders = result.scalar() or 0
    
    # Completed orders
    stmt = select(func.count(Order.id)).where(
        Order.seller_id == seller.id,
        Order.status == OrderStatus.DELIVERED,
    )
    result = await session.execute(stmt)
    completed_orders = result.scalar() or 0
    
    # Total revenue
    stmt = select(func.sum(Order.total_amount)).where(
        Order.seller_id == seller.id,
        Order.status == OrderStatus.DELIVERED,
    )
    result = await session.execute(stmt)
    total_revenue = result.scalar() or 0
    
    # This month revenue
    stmt = select(func.sum(Order.total_amount)).where(
        Order.seller_id == seller.id,
        Order.status == OrderStatus.DELIVERED,
        Order.created_at >= month_ago,
    )
    result = await session.execute(stmt)
    month_revenue = result.scalar() or 0
    
    # Total views
    stmt = select(func.sum(Product.view_count)).where(Product.seller_id == seller.id)
    result = await session.execute(stmt)
    total_views = result.scalar() or 0
    
    # Total sold
    stmt = select(func.sum(Product.sold_count)).where(Product.seller_id == seller.id)
    result = await session.execute(stmt)
    total_sold = result.scalar() or 0
    
    # Conversion rate
    conversion = (total_sold / total_views * 100) if total_views > 0 else 0
    
    text = (
        f"📊 <b>Statistika</b>\n\n"
        f"📦 <b>Mahsulotlar:</b>\n"
        f"├ Jami: {total_products} ta\n"
        f"├ Faol: {active_products} ta\n"
        f"├ Ko'rishlar: {total_views}\n"
        f"└ Sotilgan: {total_sold} ta\n\n"
        f"📋 <b>Buyurtmalar:</b>\n"
        f"├ Jami: {total_orders} ta\n"
        f"└ Yakunlangan: {completed_orders} ta\n\n"
        f"💰 <b>Daromad:</b>\n"
        f"├ Jami: {total_revenue:,.0f} so'm\n"
        f"└ Bu oy: {month_revenue:,.0f} so'm\n\n"
        f"📈 Konversiya: {conversion:.1f}%\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📦 Top mahsulotlar", callback_data="seller:top_products"),
        ],
        [
            InlineKeyboardButton(text="📅 Bu hafta", callback_data="seller:analytics:week"),
            InlineKeyboardButton(text="📅 Bu oy", callback_data="seller:analytics:month"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:dashboard"),
        ],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "seller:top_products")
async def show_top_products(callback: CallbackQuery, user: User, session) -> None:
    """Show top selling products."""
    from sqlalchemy import select
    
    seller = user.seller_profile
    
    stmt = (
        select(Product)
        .where(Product.seller_id == seller.id)
        .order_by(Product.sold_count.desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    
    if not products:
        await callback.answer("Mahsulotlar yo'q!", show_alert=True)
        return
    
    text = "🏆 <b>Top mahsulotlar</b>\n\n"
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, product in enumerate(products):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        text += (
            f"{medal} <b>{product.name[:25]}</b>\n"
            f"    💰 {product.price:,.0f} so'm | 🛒 {product.sold_count} ta sotilgan\n\n"
        )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:analytics")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "seller:analytics:week")
async def week_analytics(callback: CallbackQuery, user: User, session) -> None:
    """Show weekly analytics."""
    from sqlalchemy import select, func
    from datetime import datetime, timedelta
    
    seller = user.seller_profile
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    # Week orders
    stmt = select(func.count(Order.id)).where(
        Order.seller_id == seller.id,
        Order.created_at >= week_ago,
    )
    result = await session.execute(stmt)
    week_orders = result.scalar() or 0
    
    # Week revenue
    stmt = select(func.sum(Order.total_amount)).where(
        Order.seller_id == seller.id,
        Order.status == OrderStatus.DELIVERED,
        Order.created_at >= week_ago,
    )
    result = await session.execute(stmt)
    week_revenue = result.scalar() or 0
    
    # Week views
    stmt = select(func.sum(Product.view_count)).where(Product.seller_id == seller.id)
    result = await session.execute(stmt)
    views = result.scalar() or 0
    
    text = (
        f"📅 <b>Bu hafta statistikasi</b>\n\n"
        f"📋 Buyurtmalar: {week_orders} ta\n"
        f"💰 Daromad: {week_revenue:,.0f} so'm\n"
        f"📈 O'rtacha kunlik: {week_revenue/7:,.0f} so'm\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:analytics")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "seller:analytics:month")
async def month_analytics(callback: CallbackQuery, user: User, session) -> None:
    """Show monthly analytics."""
    from sqlalchemy import select, func
    from datetime import datetime, timedelta
    
    seller = user.seller_profile
    month_ago = datetime.utcnow() - timedelta(days=30)
    
    # Month orders
    stmt = select(func.count(Order.id)).where(
        Order.seller_id == seller.id,
        Order.created_at >= month_ago,
    )
    result = await session.execute(stmt)
    month_orders = result.scalar() or 0
    
    # Month revenue
    stmt = select(func.sum(Order.total_amount)).where(
        Order.seller_id == seller.id,
        Order.status == OrderStatus.DELIVERED,
        Order.created_at >= month_ago,
    )
    result = await session.execute(stmt)
    month_revenue = result.scalar() or 0
    
    # Completed rate
    completed_stmt = select(func.count(Order.id)).where(
        Order.seller_id == seller.id,
        Order.status == OrderStatus.DELIVERED,
        Order.created_at >= month_ago,
    )
    result = await session.execute(completed_stmt)
    completed = result.scalar() or 0
    
    completion_rate = (completed / month_orders * 100) if month_orders > 0 else 0
    
    text = (
        f"📅 <b>Bu oy statistikasi</b>\n\n"
        f"📋 Buyurtmalar: {month_orders} ta\n"
        f"✅ Yakunlangan: {completed} ta ({completion_rate:.0f}%)\n"
        f"💰 Daromad: {month_revenue:,.0f} so'm\n"
        f"📈 O'rtacha kunlik: {month_revenue/30:,.0f} so'm\n"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="seller:analytics")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
