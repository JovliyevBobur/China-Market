"""
states.py
FSM (Finite State Machine) uchun state'lar shu faylda e'lon qilinadi.
"""

from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    """
    Foydalanuvchini ro'yxatdan o'tkazish uchun kerak bo'ladigan bosqichlar.
    """

    choose_language = State()  # Til tanlash
    first_name = State()  # Ism kiritish
    last_name = State()  # Familiya kiritish
    region = State()  # Viloyat tanlash
    district = State()  # Tuman tanlash
    phone = State()  # Telefon raqam yuborish (contact)


