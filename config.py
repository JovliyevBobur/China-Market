"""
config.py
Bu yerda bot konfiguratsiyasi, xususan TOKEN saqlanadi.
TOKEN ni xavfsizlik uchun alohida faylda saqlash tavsiya etiladi.
"""

from dataclasses import dataclass
import os


@dataclass
class BotConfig:
    """
    Bot uchun asosiy konfiguratsiya dataclass ko'rinishida.
    Hozircha faqat TOKEN saqlanadi, lekin keyinchalik kengaytirish mumkin.
    """

    token: str


def load_config() -> BotConfig:
    """
    Atrof-muhit o'zgaruvchisidan (environment variable) yoki to'g'ridan-to'g'ri
    matndan TOKEN ni yuklaydi.

    ENG MUHIMI:
        - Amaliyotda TOKEN ni kod ichida ochiq qoldirmang.
        - Windowsda PowerShell orqali vaqtinchalik ishga tushirish uchun:
              $env:BOT_TOKEN="SIZNING_TOKENINGIZ"
    """

    token = os.getenv("BOT_TOKEN", "8097749020:AAGwMMNypbp4lno4yPa1pX7EZ1wojMMAe0Y")
    return BotConfig(token=token)


