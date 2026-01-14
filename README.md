## Telegram bot (aiogram 3.x) – Ro'yxatdan o'tish va asosiy menyu

Bu loyihada aiogram 3.x asosida yozilgan oddiy Telegram bot mavjud. Bot foydalanuvchini:

- **Til tanlash** (🇺🇿, 🇬🇧, 🇷🇺)
- **Ism, familiya kiritish**
- **Viloyat va tuman tanlash** (button orqali)
- **Telefon raqamni kontakt sifatida yuborish**

bosqichlaridan o'tkazadi va:

- **“Ro'yxatdan o'tish muvaffaqiyatli yakunlandi ✅”** xabarini yuboradi
- Asosiy menyu tugmalarini chiqaradi.


### Fayllar tuzilmasi (asosiylari)

- `main.py` – asosiy bot kodi, handlerlar va FSM oqimi
- `config.py` – bot tokeni konfiguratsiyasi
- `states.py` – FSM (RegistrationStates) holatlari
- `keyboards.py` – barcha ReplyKeyboard va InlineKeyboard tugmalari
- `requirements.txt` – kerakli Python kutubxonalari ro'yxati


### O'rnatish va ishga tushirish

1. **Virtual muhit (ixtiyoriy, lekin tavsiya etiladi)**  
   PowerShell:

   ```powershell
   cd "C:\Users\9-sinf\Downloads\China-Market"
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Kutubxonalarni o'rnatish**

   ```powershell
   pip install -r requirements.txt
   ```

3. **BOT TOKEN ni o'rnatish**

   `config.py` ichidagi `PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE` o'rniga tokenni yozishingiz yoki PowerShell orqali atrof-muhitga o'rnatishingiz mumkin:

   ```powershell
   $env:BOT_TOKEN="SIZNING_TELEGRAM_BOT_TOKENINGIZ"
   ```

4. **Botni ishga tushirish**

   ```powershell
   python main.py
   ```

5. **Telegram'da /start buyrug'i**  
   Botni ishga tushirgandan so'ng, Telegram'da botingizga kirib, `/start` yozing va ko'rsatmalarga amal qiling.

