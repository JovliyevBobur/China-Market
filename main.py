"""
main.py

Asosiy Telegram bot dasturi.

Talablar:
    - aiogram (so'nggi versiya, v3.x) asosida
    - FSM (Finite State Machine) orqali ro'yxatdan o'tkazish
    - Til tanlash, viloyat/tuman tanlash, telefon raqamni kontakt orqali yuborish
    - Ro'yxatdan o'tgach asosiy menyu tugmalari chiqarish
"""

import asyncio
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentType

from config import load_config
from states import RegistrationStates
from keyboards import (
    language_keyboard,
    regions_keyboard,
    districts_keyboard,
    phone_request_keyboard,
    main_menu_keyboard,
    UZB_REGIONS,
)


# Oddiy "xotira" sifatida ishlatiladigan lug'at:
# Foydalanuvchi ID => ma'lumotlar
users_data: Dict[int, Dict[str, Any]] = {}


async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    /start komandasi uchun handler.
    Foydalanuvchini kutib oladi va til tanlash klaviaturasini chiqaradi.
    """

    await state.clear()  # Avvalgi barcha state'larni tozalab yuboramiz

    await message.answer(
        "Assalomu alaykum! Botimizga xush kelibsiz 👋\n\n"
        "Iltimos, tilni tanlang:",
        reply_markup=language_keyboard(),
    )

    # FSM ni til tanlash holatiga o'tkazamiz
    await state.set_state(RegistrationStates.choose_language)


async def choose_language(message: Message, state: FSMContext) -> None:
    """
    Foydalanuvchi tilni tanlaydi.
    Tanlangan tilni FSM context (yoki users_data) orqali saqlaymiz.
    """

    text = message.text

    # Tilni oddiy ko'rinishda saqlab qo'yamiz
    if "O'zbek" in text:
        lang = "uz"
    elif "English" in text:
        lang = "en"
    elif "Русский" in text or "Рус" in text:
        lang = "ru"
    else:
        await message.answer(
            "Iltimos, berilgan tugmalardan birini tanlang.",
            reply_markup=language_keyboard(),
        )
        return

    # FSM context ichida saqlash
    await state.update_data(language=lang)

    # Qo'shimcha ravishda users_data lug'atida ham saqlashimiz mumkin
    users_data[message.from_user.id] = {"language": lang}

    await message.answer(
        "Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationStates.first_name)


async def get_first_name(message: Message, state: FSMContext) -> None:
    """
    Foydalanuvchi ismini qabul qilamiz.
    """

    first_name = message.text.strip()
    if len(first_name) < 2:
        await message.answer("Ism juda qisqa, qaytadan kiriting:")
        return

    await state.update_data(first_name=first_name)
    users_data.setdefault(message.from_user.id, {})
    users_data[message.from_user.id]["first_name"] = first_name

    await message.answer("Familiyangizni kiriting:")
    await state.set_state(RegistrationStates.last_name)


async def get_last_name(message: Message, state: FSMContext) -> None:
    """
    Foydalanuvchi familiyasini qabul qilamiz.
    """

    last_name = message.text.strip()
    if len(last_name) < 2:
        await message.answer("Familiya juda qisqa, qaytadan kiriting:")
        return

    await state.update_data(last_name=last_name)
    users_data.setdefault(message.from_user.id, {})
    users_data[message.from_user.id]["last_name"] = last_name

    await message.answer(
        "Viloyatingizni tanlang:",
        reply_markup=regions_keyboard(),
    )
    await state.set_state(RegistrationStates.region)


async def choose_region(message: Message, state: FSMContext) -> None:
    """
    Viloyat tanlash.
    Tanlangan viloyatga qarab mos tumanlar klaviaturasi chiqariladi.
    """

    region = message.text.strip()
    if region not in UZB_REGIONS:
        await message.answer(
            "Iltimos, tugmalardan foydalanib viloyatni tanlang.",
            reply_markup=regions_keyboard(),
        )
        return

    await state.update_data(region=region)
    users_data.setdefault(message.from_user.id, {})
    users_data[message.from_user.id]["region"] = region

    await message.answer(
        "Tumaningizni tanlang:",
        reply_markup=districts_keyboard(region),
    )
    await state.set_state(RegistrationStates.district)


async def choose_district(message: Message, state: FSMContext) -> None:
    """
    Tanlangan viloyat ichidan tuman tanlash.
    """

    data = await state.get_data()
    region = data.get("region")
    districts = UZB_REGIONS.get(region, [])
    district = message.text.strip()

    if district not in districts:
        await message.answer(
            "Iltimos, tugmalardan foydalanib tumanni tanlang.",
            reply_markup=districts_keyboard(region),
        )
        return

    await state.update_data(district=district)
    users_data.setdefault(message.from_user.id, {})
    users_data[message.from_user.id]["district"] = district

    await message.answer(
        "Telefon raqamingizni kontakt sifatida yuboring:",
        reply_markup=phone_request_keyboard(),
    )
    await state.set_state(RegistrationStates.phone)


async def get_phone(message: Message, state: FSMContext) -> None:
    """
    Telefon raqamni faqat kontakt ko'rinishida qabul qilamiz.
    """

    if message.content_type != ContentType.CONTACT or message.contact is None:
        await message.answer(
            "Iltimos, telefon raqamingizni '📱 Raqamni yuborish' tugmasi yordamida yuboring.",
            reply_markup=phone_request_keyboard(),
        )
        return

    phone_number = message.contact.phone_number

    await state.update_data(phone=phone_number)
    users_data.setdefault(message.from_user.id, {})
    users_data[message.from_user.id]["phone"] = phone_number

    # Barcha ma'lumotlarni olish
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    region = data.get("region")
    district = data.get("district")

    # Ro'yxatdan o'tish yakunlanganligi haqida xabar
    await message.answer(
        "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi ✅\n\n"
        f"Ism: {first_name}\n"
        f"Familiya: {last_name}\n"
        f"Viloyat: {region}\n"
        f"Tuman: {district}\n"
        f"Telefon: {phone_number}",
        reply_markup=main_menu_keyboard(),
    )

    # State ni tozalaymiz, lekin users_data da ma'lumotlar qoladi
    await state.clear()


async def main() -> None:
    """
    Botni ishga tushiruvchi asosiy funksiya.
    """

    config = load_config()
    bot = Bot(token=config.token, parse_mode="HTML")
    dp = Dispatcher()

    # Handlerlarni ro'yxatdan o'tkazish
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(choose_language, RegistrationStates.choose_language)
    dp.message.register(get_first_name, RegistrationStates.first_name)
    dp.message.register(get_last_name, RegistrationStates.last_name)
    dp.message.register(choose_region, RegistrationStates.region)
    dp.message.register(choose_district, RegistrationStates.district)
    dp.message.register(get_phone, RegistrationStates.phone)

    # Botni polling rejimida ishga tushiramiz
    print("Bot ishga tushmoqda...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi.")


