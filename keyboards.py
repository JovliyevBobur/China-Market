"""
keyboards.py
Bu faylda barcha ReplyKeyboard va InlineKeyboard tugmalari jamlanadi.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# ============================
#  TIL TANLASH TUGMALARI
# ============================


def language_keyboard() -> ReplyKeyboardMarkup:
    """
    Foydalanuvchi uchun til tanlash klaviaturasi.
    """

    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbek")],
            [KeyboardButton(text="🇬🇧 English")],
            [KeyboardButton(text="🇷🇺 Русский")],
        ],
    )
    return kb


# ============================
#  VILOYATLAR VA TUMANLAR
# ============================

# O'zbekiston viloyatlari va ularga tegishli tumanlar lug'ati
UZB_REGIONS = {
    "Toshkent shahri": [
        "Chilonzor",
        "Mirzo Ulug'bek",
        "Yunusobod",
        "Shayxontohur",
        "Yakkasaroy",
        "Olmazor",
        "Uchtepa",
    ],
    "Toshkent viloyati": [
        "Bekobod",
        "Angren",
        "Chirchiq",
        "Ohangaron",
        "Nurafshon",
    ],
    "Andijon": [
        "Andijon shahri",
        "Asaka",
        "Jalaquduq",
        "Qo'rg'ontepa",
    ],
    "Farg'ona": [
        "Farg'ona shahri",
        "Qo'qon",
        "Marg'ilon",
        "Quva",
    ],
    "Namangan": [
        "Namangan shahri",
        "Chortoq",
        "Chust",
        "Uchqo'rg'on",
    ],
    "Samarqand": [
        "Samarqand shahri",
        "Urgut",
        "Kattaqo'rg'on",
    ],
    "Buxoro": [
        "Buxoro shahri",
        "G'ijduvon",
        "Qorovulbozor",
    ],
    "Xorazm": [
        "Urganch",
        "Xiva",
        "Xonqa",
    ],
    "Qashqadaryo": [
        "Qarshi",
        "Shahrisabz",
        "Chiroqchi",
    ],
    "Surxondaryo": [
        "Termiz",
        "Denov",
        "Sherobod",
    ],
    "Jizzax": [
        "Jizzax shahri",
        "Zomin",
        "G'allaorol",
    ],
    "Sirdaryo": [
        "Guliston",
        "Yangiyer",
        "Sirdaryo tumani",
    ],
    "Navoiy": [
        "Navoiy shahri",
        "Zarafshon",
        "Karmana",
    ],
    "Qoraqalpog'iston Respublikasi": [
        "Nukus",
        "Taxiatosh",
        "Xo'jayli",
    ],
}


def regions_keyboard() -> ReplyKeyboardMarkup:
    """
    Viloyatlar uchun ReplyKeyboard.
    Har bir qatorga 2-3 tadan viloyat nomlari joylashtiriladi.
    """

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for i, region in enumerate(UZB_REGIONS.keys(), start=1):
        row.append(KeyboardButton(text=region))
        if i % 2 == 0:
            kb.keyboard.append(row)
            row = []
    if row:
        kb.keyboard.append(row)
    return kb


def districts_keyboard(region_name: str) -> ReplyKeyboardMarkup:
    """
    Tanlangan viloyatga tegishli tumanlarni chiqaruvchi ReplyKeyboard.
    """

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    districts = UZB_REGIONS.get(region_name, [])
    row = []
    for i, district in enumerate(districts, start=1):
        row.append(KeyboardButton(text=district))
        if i % 2 == 0:
            kb.keyboard.append(row)
            row = []
    if row:
        kb.keyboard.append(row)
    return kb


# ============================
#  TELEFON RAQAM TUGMASI
# ============================


def phone_request_keyboard() -> ReplyKeyboardMarkup:
    """
    Telefon raqamini kontakt sifatida yuborish uchun tugma.
    """

    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]
        ],
    )
    return kb


# ============================
#  ASOSIY MENYU TUGMALARI
# ============================


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Ro'yxatdan o'tgan foydalanuvchi uchun asosiy menyu.
    """

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.keyboard = [
        [
            KeyboardButton(
                text="✅ 👗 Kiyim-kechak, sport kiyimlari, ichki kiyimlar"
            )
        ],
        [KeyboardButton(text="✅ 👟 Oyoq kiyimlar")],
        [KeyboardButton(text="✅ 🎒 Sumka, ryukzak, chamadon")],
        [
            KeyboardButton(
                text="✅ 🛋 Uy-ro'zg'or buyumlari (parda, choyshab, gilamcha, dekor)"
            )
        ],
        [KeyboardButton(text="✅ 🧸 Bolalar o'yinchoqlari")],
        [
            KeyboardButton(
                text="✅ ⌨️ Kompyuter aksessuarlari (klaviatura, sichqoncha, usb, ringlight)"
            )
        ],
        [
            KeyboardButton(
                text="✅ 📷 Kamera, stativ, mikrofonlar (SIM kartasiz)"
            )
        ],
        [
            KeyboardButton(
                text="✅ 🛠 Elektr instrumentlar (SIM, suyuqlik, gazsiz bo'lsa)"
            )
        ],
        [
            KeyboardButton(
                text="✅ 💡 Yorug'lik chiroqlari, LED lenta va lampalar"
            )
        ],
        [
            KeyboardButton(
                text="✅ 🪞 Go'zallik buyumlari (fön, fen-cho'tkalar, aksessuarlar)"
            )
        ],
        [
            KeyboardButton(
                text="✅ 📚 Kitob, daftar, qalam, rasm chizish anjomlari"
            )
        ],
        [
            KeyboardButton(
                text="✅ 🧳 Sayohat uchun kerakli buyumlar"
            )
        ],
        [
            KeyboardButton(
                text="✅ 📺 Monitor, ekranlar (SIM yoki signal ushlovchi qurilmasiz)"
            )
        ],
    ]

    return kb


# ============================
#  YORDAMCHI INLINE TUGMALAR
# (hozircha shart emas, lekin
#  keyinchalik kerak bo'lishi mumkin)
# ============================


def simple_back_inline(text: str = "⬅️ Ortga", callback_data: str = "back") -> InlineKeyboardMarkup:
    """
    Oddiy "Ortga" tugmasi uchun namuna InlineKeyboard.
    Hozirgi loyihada ishlatilmasligi mumkin, lekin tayyor turadi.
    """

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback_data)]
        ]
    )
    return kb


