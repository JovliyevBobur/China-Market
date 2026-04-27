"""
🆘 Support Handler Module

Help and support for users.
"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.database.models import User
from app.states.user_states import SupportStates

router = Router(name="support")


@router.message(Command("help"))
@router.message(Command("support"))
@router.message(F.text.in_(["🆘 Yordam", "🆘 Помощь", "🆘 Help"]))
async def show_help(message: Message) -> None:
    """Show help menu."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    text = (
        "🆘 <b>Yordam markazi</b>\n\n"
        "Quyidagi bo'limlardan birini tanlang:\n\n"
        "❓ <b>FAQ</b> - Tez-tez so'raladigan savollar\n"
        "📞 <b>Bog'lanish</b> - Admin bilan bog'lanish\n"
        "📖 <b>Qo'llanma</b> - Botdan foydalanish\n"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❓ FAQ", callback_data="help:faq"),
            InlineKeyboardButton(text="📖 Qo'llanma", callback_data="help:guide"),
        ],
        [
            InlineKeyboardButton(text="📞 Admin bilan bog'lanish", callback_data="help:contact"),
        ],
        [
            InlineKeyboardButton(text="📝 Taklif/Shikoyat", callback_data="help:feedback"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main"),
        ],
    ])
    
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "help:faq")
async def show_faq(callback: CallbackQuery) -> None:
    """Show FAQ."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    text = (
        "❓ <b>Tez-tez so'raladigan savollar</b>\n\n"
        
        "🔹 <b>Qanday buyurtma beraman?</b>\n"
        "Katalogdan mahsulotni tanlab, savatga qo'shing va "
        "buyurtma berish tugmasini bosing.\n\n"
        
        "🔹 <b>To'lov qanday amalga oshiriladi?</b>\n"
        "Click, Payme yoki Telegram Stars orqali to'lov qilishingiz mumkin.\n\n"
        
        "🔹 <b>Yetkazib berish qancha vaqt oladi?</b>\n"
        "Toshkent shahriga 1-2 kun, viloyatlarga 2-5 kun.\n\n"
        
        "🔹 <b>Mahsulotni qaytarish mumkinmi?</b>\n"
        "Ha, 14 kun ichida qaytarish mumkin (ishlatilmagan holatda).\n\n"
        
        "🔹 <b>Sotuvchi bo'lish mumkinmi?</b>\n"
        "Ha! /seller buyrug'ini yuboring.\n"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="help:back")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "help:guide")
async def show_guide(callback: CallbackQuery) -> None:
    """Show user guide."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    text = (
        "📖 <b>Foydalanish qo'llanmasi</b>\n\n"
        
        "🛒 <b>Xarid qilish:</b>\n"
        "1. /catalog - Mahsulotlarni ko'ring\n"
        "2. Mahsulotni tanlang\n"
        "3. Savatga qo'shing\n"
        "4. /cart - Savatni tekshiring\n"
        "5. Buyurtma bering va to'lang\n\n"
        
        "🔍 <b>Qidirish:</b>\n"
        "/search - Mahsulot izlash\n"
        "/filter - Filterlar bilan qidirish\n\n"
        
        "👤 <b>Profil:</b>\n"
        "/profile - Profil sozlamalari\n"
        "/orders - Buyurtmalar tarixi\n\n"
        
        "🏪 <b>Sotuvchi bo'lish:</b>\n"
        "/seller - Sotuvchi paneli\n"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="help:back")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "help:contact")
async def contact_admin(callback: CallbackQuery, state: FSMContext) -> None:
    """Start contacting admin."""
    await state.set_state(SupportStates.waiting_message)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="help:cancel")],
    ])
    
    await callback.message.edit_text(
        "📞 <b>Admin bilan bog'lanish</b>\n\n"
        "Xabaringizni yozing va biz sizga tez orada javob beramiz.\n\n"
        "<i>Iltimos, muammoni batafsil yozing.</i>",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(SupportStates.waiting_message)
async def process_support_message(message: Message, user: User, state: FSMContext) -> None:
    """Process support message and notify admins."""
    from app.loader import bot
    
    user_message = message.text or message.caption or "Media xabar"
    
    # Notify all admins
    admin_text = (
        f"📩 <b>Yangi xabar!</b>\n\n"
        f"👤 Foydalanuvchi: {user.mention}\n"
        f"🆔 ID: <code>{user.telegram_id}</code>\n"
        f"📱 Telefon: {user.phone or 'Noma'lum'}\n\n"
        f"💬 <b>Xabar:</b>\n{user_message[:500]}"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📝 Javob yozish",
            callback_data=f"admin:reply:{user.telegram_id}",
        )],
    ])
    
    sent_count = 0
    for admin_id in settings.admin_ids:
        try:
            # Forward original message if possible
            if message.text:
                await bot.send_message(
                    chat_id=admin_id,
                    text=admin_text,
                    reply_markup=admin_keyboard,
                )
            else:
                # Forward media
                await message.forward(chat_id=admin_id)
                await bot.send_message(
                    chat_id=admin_id,
                    text=admin_text,
                    reply_markup=admin_keyboard,
                )
            sent_count += 1
        except Exception:
            pass
    
    await state.clear()
    
    from app.keyboards.reply.main_menu import create_main_menu
    
    await message.answer(
        "✅ <b>Xabaringiz yuborildi!</b>\n\n"
        "Adminlarimiz tez orada sizga javob berishadi.\n"
        "Iltimos, kuting.",
        reply_markup=create_main_menu(),
    )


@router.callback_query(F.data == "help:feedback")
async def start_feedback(callback: CallbackQuery, state: FSMContext) -> None:
    """Start feedback process."""
    await state.set_state(SupportStates.waiting_feedback)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="help:cancel")],
    ])
    
    await callback.message.edit_text(
        "📝 <b>Taklif yoki Shikoyat</b>\n\n"
        "Fikringizni yozing. Biz har bir taklifni ko'rib chiqamiz!\n\n"
        "<i>Taklif yoki shikoyatingizni batafsil yozing.</i>",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(SupportStates.waiting_feedback)
async def process_feedback(message: Message, user: User, state: FSMContext) -> None:
    """Process feedback."""
    from app.loader import bot
    
    feedback = message.text
    
    # Notify admins
    admin_text = (
        f"📝 <b>Yangi taklif/shikoyat!</b>\n\n"
        f"👤 Foydalanuvchi: {user.mention}\n"
        f"🆔 ID: <code>{user.telegram_id}</code>\n\n"
        f"💬 <b>Matn:</b>\n{feedback[:1000]}"
    )
    
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(chat_id=admin_id, text=admin_text)
        except Exception:
            pass
    
    await state.clear()
    
    from app.keyboards.reply.main_menu import create_main_menu
    
    await message.answer(
        "✅ <b>Rahmat!</b>\n\n"
        "Fikringiz qabul qilindi. Biz har doim yaxshilanish ustida ishlaymiz!",
        reply_markup=create_main_menu(),
    )


@router.callback_query(F.data == "help:cancel")
async def cancel_support(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel support/feedback."""
    await state.clear()
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❓ FAQ", callback_data="help:faq"),
            InlineKeyboardButton(text="📖 Qo'llanma", callback_data="help:guide"),
        ],
        [
            InlineKeyboardButton(text="📞 Admin bilan bog'lanish", callback_data="help:contact"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main"),
        ],
    ])
    
    await callback.message.edit_text(
        "🆘 <b>Yordam markazi</b>\n\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "help:back")
async def back_to_help(callback: CallbackQuery) -> None:
    """Go back to help menu."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❓ FAQ", callback_data="help:faq"),
            InlineKeyboardButton(text="📖 Qo'llanma", callback_data="help:guide"),
        ],
        [
            InlineKeyboardButton(text="📞 Admin bilan bog'lanish", callback_data="help:contact"),
        ],
        [
            InlineKeyboardButton(text="📝 Taklif/Shikoyat", callback_data="help:feedback"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main"),
        ],
    ])
    
    await callback.message.edit_text(
        "🆘 <b>Yordam markazi</b>\n\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=keyboard,
    )
    await callback.answer()
