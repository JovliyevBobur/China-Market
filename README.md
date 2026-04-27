# 🛒 China Market Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![aiogram](https://img.shields.io/badge/aiogram-3.24+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Professional Telegram Marketplace Bot**

[O'zbek](#uzbek) | [English](#english) | [Русский](#russian)

</div>

---

## 📋 Mundarija

- [Xususiyatlar](#-xususiyatlar)
- [Texnologiyalar](#-texnologiyalar)
- [O'rnatish](#-ornatish)
- [Konfiguratsiya](#-konfiguratsiya)
- [Ishga tushirish](#-ishga-tushirish)
- [API Hujjatlar](#-api-hujjatlar)
- [Loyiha Strukturasi](#-loyiha-strukturasi)

---

## ✨ Xususiyatlar

### 👤 Foydalanuvchilar uchun
- ✅ Oson ro'yxatdan o'tish (telefon raqami bilan)
- ✅ Mahsulotlar katalogi (kategoriyalar bo'yicha)
- ✅ Kuchli qidiruv tizimi
- ✅ Savat boshqaruvi
- ✅ Buyurtma berish va kuzatish
- ✅ Ko'p kanalli to'lov (Telegram Stars, Click, Payme)
- ✅ Sharhlar va baholash
- ✅ Sevimli mahsulotlar
- ✅ Ko'p tilli interfeys (UZ, RU, EN)

### 🏪 Sotuvchilar uchun
- ✅ Sotuvchi sifatida ro'yxatdan o'tish
- ✅ Mahsulot qo'shish/tahrirlash/o'chirish
- ✅ Buyurtmalarni boshqarish
- ✅ Statistika va analitika
- ✅ Daromad hisoboti
- ✅ Mijozlar bilan muloqot

### 👑 Adminlar uchun
- ✅ To'liq dashboard
- ✅ Foydalanuvchilarni boshqarish
- ✅ Sotuvchilarni tasdiqlash
- ✅ Mahsulotlarni moderatsiya
- ✅ Kategoriyalarni boshqarish
- ✅ Xabar tarqatish (broadcast)
- ✅ Hisobotlar

---

## 🛠 Texnologiyalar

| Kategoriya | Texnologiya |
|------------|-------------|
| Framework | aiogram 3.24+ |
| Til | Python 3.11+ |
| Database | PostgreSQL 15+ |
| Cache | Redis 7+ |
| ORM | SQLAlchemy 2.0+ |
| Validation | Pydantic 2.0+ |
| Migration | Alembic |
| Security | JWT, bcrypt, cryptography |
| Container | Docker & Docker Compose |

---

## 📦 O'rnatish

### Talablar
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (ixtiyoriy)

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/chinamarket/telegram-bot.git
cd telegram-bot
```

### 2. Virtual muhit yaratish

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/MacOS
source .venv/bin/activate
```

### 3. Bog'liqliklarni o'rnatish

```bash
# Production
pip install -r requirements.txt

# Development
pip install -r requirements-dev.txt
```

### 4. Environment variables sozlash

```bash
cp .env.example .env
# .env faylini tahrirlang
```

### 5. Ma'lumotlar bazasini sozlash

```bash
# Migration yaratish
alembic revision --autogenerate -m "Initial migration"

# Migrationni qo'llash
alembic upgrade head
```

---

## ⚙️ Konfiguratsiya

`.env` faylida quyidagi o'zgaruvchilarni sozlang:

```env
# Bot
BOT_TOKEN=your_bot_token
ADMIN_IDS=123456789

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=china_market
DB_USER=postgres
DB_PASSWORD=your_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your_secret_key
```

---

## 🚀 Ishga tushirish

### Development rejimida

```bash
python -m app.main
```

### Docker bilan

```bash
# Build va run
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f bot
```

### Production rejimida

```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

---

## 📁 Loyiha Strukturasi

```
china_market_bot/
├── app/
│   ├── main.py              # Entry point
│   ├── loader.py            # Bot va Dispatcher
│   ├── config/              # Konfiguratsiya
│   ├── database/            # Database modellari va repositorylar
│   ├── handlers/            # Telegram handlerlari
│   ├── keyboards/           # Klaviaturalar
│   ├── states/              # FSM holatlar
│   ├── middlewares/         # Middlewarelar
│   ├── filters/             # Maxsus filterlar
│   ├── services/            # Biznes logika
│   ├── utils/               # Yordamchi funksiyalar
│   ├── callbacks/           # Callback data
│   └── locales/             # Tarjimalar
├── migrations/              # Alembic migrations
├── tests/                   # Testlar
├── docker/                  # Docker fayllar
├── scripts/                 # Utility scriptlar
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── alembic.ini
└── README.md
```

---

## 🧪 Testlar

```bash
# Barcha testlarni bajarish
pytest

# Coverage bilan
pytest --cov=app --cov-report=html

# Faqat unit testlar
pytest -m unit

# Faqat integration testlar
pytest -m integration
```

---

## 📝 API Hujjatlar

Bot quyidagi buyruqlarni qo'llab-quvvatlaydi:

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni ishga tushirish |
| `/catalog` | Mahsulotlar katalogi |
| `/search` | Mahsulot qidirish |
| `/cart` | Savat |
| `/orders` | Buyurtmalar tarixi |
| `/profile` | Profil sozlamalari |
| `/help` | Yordam |
| `/language` | Til o'zgartirish |

---

## 🔒 Xavfsizlik

- ✅ Input validation (Pydantic)
- ✅ SQL injection himoyasi (SQLAlchemy ORM)
- ✅ Rate limiting
- ✅ JWT authentication
- ✅ Ma'lumotlarni shifrlash
- ✅ XSS himoyasi

---

## 📄 Litsenziya

MIT License - batafsil [LICENSE](LICENSE) faylida

---

## 👥 Hissa qo'shish

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/amazing`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add amazing feature'`)
4. Push qiling (`git push origin feature/amazing`)
5. Pull Request oching

---

## 📞 Aloqa

- Telegram: [@china_market_support](https://t.me/china_market_support)
- Email: support@chinamarket.uz

---

<div align="center">

**Made with ❤️ in Uzbekistan**

*© 2026 China Market. Barcha huquqlar himoyalangan.*

</div>
