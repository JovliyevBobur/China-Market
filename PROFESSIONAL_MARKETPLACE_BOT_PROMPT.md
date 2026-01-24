# 🛒 Professional Telegram Marketplace Bot Development Prompt

## Claude Opus AI uchun Professional Prompt

> **Maqsad**: Zamonaviy, xavfsiz va to'liq funksiyali Telegram bozor botini aiogram 3+ yordamida yaratish

---

## 📋 PROMPT BOSHLANISHI

```
Sen professional Python dasturchi va Telegram bot ekspertisan. Senga zamonaviy, xavfsiz va to'liq funksiyali Telegram Marketplace (Bozor) botini yaratish vazifasi yuklanadi.

### 🎯 LOYIHA MAQSADI:
Foydalanuvchilar mahsulotlarni xarid qilishi, sotuvchilar esa o'z mahsulotlarini joylashtirishi mumkin bo'lgan to'liq funksiyali e-commerce Telegram botini yaratish.

### 🛠️ TEXNOLOGIYALAR STEKI:

#### Asosiy Framework:
- **aiogram 3.x** (3.24.0 yoki undan yuqori)
- **Python 3.11+**
- **asyncio** - asinxron dasturlash

#### Ma'lumotlar Bazasi:
- **PostgreSQL** - asosiy ma'lumotlar bazasi
- **SQLAlchemy 2.0+** - asinxron ORM
- **Alembic** - migration uchun
- **Redis** - FSM storage, caching va session management uchun

#### Qo'shimcha Kutubxonalar:
- **pydantic** - data validation
- **python-dotenv** - environment variables
- **aiohttp** - asinxron HTTP so'rovlar
- **cryptography** - shifrlash
- **bcrypt** - parol hashing
- **PyJWT** - JSON Web Tokens
- **aiofiles** - asinxron fayl operatsiyalari
- **Pillow** - rasm ishlov berish
- **babel** - i18n/l10n

---

## 📁 LOYIHA STRUKTURASI

Quyidagi modular strukturani yarating:

```
china_market_bot/
├── 📁 app/
│   ├── 📄 __init__.py
│   ├── 📄 main.py                    # Bot entry point
│   ├── 📄 loader.py                  # Bot, Dispatcher va boshqa global obyektlar
│   │
│   ├── 📁 config/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 settings.py            # Pydantic settings
│   │   └── 📄 constants.py           # Global konstantalar
│   │
│   ├── 📁 database/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 engine.py              # SQLAlchemy async engine
│   │   ├── 📄 session.py             # AsyncSession factory
│   │   ├── 📁 models/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 base.py            # Base model
│   │   │   ├── 📄 user.py            # User model
│   │   │   ├── 📄 product.py         # Product model
│   │   │   ├── 📄 category.py        # Category model
│   │   │   ├── 📄 order.py           # Order model
│   │   │   ├── 📄 cart.py            # Cart model
│   │   │   ├── 📄 review.py          # Review model
│   │   │   ├── 📄 payment.py         # Payment model
│   │   │   └── 📄 seller.py          # Seller model
│   │   └── 📁 repositories/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 base_repo.py       # Abstract base repository
│   │       ├── 📄 user_repo.py
│   │       ├── 📄 product_repo.py
│   │       ├── 📄 order_repo.py
│   │       └── 📄 cart_repo.py
│   │
│   ├── 📁 handlers/
│   │   ├── 📄 __init__.py
│   │   ├── 📁 user/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 start.py           # /start command
│   │   │   ├── 📄 catalog.py         # Mahsulotlar katalogi
│   │   │   ├── 📄 search.py          # Qidiruv
│   │   │   ├── 📄 cart.py            # Savat
│   │   │   ├── 📄 orders.py          # Buyurtmalar
│   │   │   ├── 📄 profile.py         # Profil
│   │   │   └── 📄 support.py         # Yordam
│   │   ├── 📁 seller/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 dashboard.py       # Sotuvchi paneli
│   │   │   ├── 📄 products.py        # Mahsulot boshqaruvi
│   │   │   ├── 📄 orders.py          # Buyurtmalar boshqaruvi
│   │   │   └── 📄 analytics.py       # Statistika
│   │   ├── 📁 admin/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 panel.py           # Admin panel
│   │   │   ├── 📄 users.py           # Foydalanuvchilar boshqaruvi
│   │   │   ├── 📄 sellers.py         # Sotuvchilar boshqaruvi
│   │   │   ├── 📄 categories.py      # Kategoriyalar
│   │   │   ├── 📄 moderation.py      # Moderatsiya
│   │   │   └── 📄 broadcast.py       # Xabar tarqatish
│   │   └── 📁 common/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 errors.py          # Xato handlerlari
│   │       └── 📄 cancel.py          # Bekor qilish handleri
│   │
│   ├── 📁 keyboards/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 reply/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 main_menu.py
│   │   │   └── 📄 user_keyboards.py
│   │   ├── 📄 inline/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 catalog_kb.py
│   │   │   ├── 📄 cart_kb.py
│   │   │   ├── 📄 order_kb.py
│   │   │   ├── 📄 pagination.py
│   │   │   └── 📄 admin_kb.py
│   │   └── 📄 builders.py            # Keyboard builder utilities
│   │
│   ├── 📁 states/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 user_states.py         # User FSM states
│   │   ├── 📄 seller_states.py       # Seller FSM states
│   │   ├── 📄 admin_states.py        # Admin FSM states
│   │   └── 📄 order_states.py        # Order FSM states
│   │
│   ├── 📁 middlewares/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 database.py            # Database session middleware
│   │   ├── 📄 user.py                # User registration middleware
│   │   ├── 📄 throttling.py          # Rate limiting
│   │   ├── 📄 logging.py             # Logging middleware
│   │   ├── 📄 i18n.py                # Internationalization
│   │   └── 📄 error_handling.py      # Global error handling
│   │
│   ├── 📁 filters/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 admin.py               # Admin filter
│   │   ├── 📄 seller.py              # Seller filter
│   │   └── 📄 chat_type.py           # Chat type filter
│   │
│   ├── 📁 services/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 user_service.py        # User business logic
│   │   ├── 📄 product_service.py     # Product business logic
│   │   ├── 📄 order_service.py       # Order business logic
│   │   ├── 📄 cart_service.py        # Cart business logic
│   │   ├── 📄 payment_service.py     # Payment processing
│   │   ├── 📄 notification_service.py # Notifications
│   │   ├── 📄 analytics_service.py   # Analytics
│   │   └── 📄 search_service.py      # Search functionality
│   │
│   ├── 📁 utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 security.py            # Security utilities
│   │   ├── 📄 validators.py          # Input validation
│   │   ├── 📄 formatters.py          # Text formatters
│   │   ├── 📄 helpers.py             # Helper functions
│   │   ├── 📄 media.py               # Media processing
│   │   └── 📄 pagination.py          # Pagination utilities
│   │
│   ├── 📁 locales/
│   │   ├── 📁 uz/
│   │   │   └── 📄 LC_MESSAGES/
│   │   ├── 📁 ru/
│   │   │   └── 📄 LC_MESSAGES/
│   │   └── 📁 en/
│   │       └── 📄 LC_MESSAGES/
│   │
│   └── 📁 callbacks/
│       ├── 📄 __init__.py
│       └── 📄 callback_data.py       # Callback data factories
│
├── 📁 migrations/                     # Alembic migrations
│   ├── 📄 env.py
│   ├── 📄 script.py.mako
│   └── 📁 versions/
│
├── 📁 tests/
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py
│   ├── 📁 unit/
│   └── 📁 integration/
│
├── 📁 docker/
│   ├── 📄 Dockerfile
│   ├── 📄 docker-compose.yml
│   └── 📄 docker-compose.prod.yml
│
├── 📁 scripts/
│   ├── 📄 init_db.py
│   └── 📄 create_admin.py
│
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 alembic.ini
├── 📄 pyproject.toml
├── 📄 requirements.txt
├── 📄 requirements-dev.txt
└── 📄 README.md
```

---

## 🔐 XAVFSIZLIK TALABLARI

### 1. Ma'lumotlar Himoyasi
```python
# Barcha maxfiy ma'lumotlarni shifrlang
from cryptography.fernet import Fernet

class DataEncryption:
    """Sezgir ma'lumotlarni shifrlash uchun klass"""
    
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Ma'lumotni shifrlash"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Ma'lumotni deshifrlash"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

### 2. Input Validation (Pydantic)
```python
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class ProductCreate(BaseModel):
    """Mahsulot yaratish uchun validation schema"""
    
    name: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    price: float = Field(..., gt=0, le=100_000_000)
    quantity: int = Field(..., ge=0, le=100_000)
    category_id: int = Field(..., gt=0)
    
    @validator('name')
    def validate_name(cls, v):
        # XSS va SQL injection himoyasi
        if re.search(r'[<>"\';()]', v):
            raise ValueError('Noto\'g\'ri belgilar aniqlandi')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        # HTML teglarini olib tashlash
        clean = re.sub(r'<[^>]+>', '', v)
        return clean.strip()
```

### 3. Rate Limiting Middleware
```python
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
import time
from collections import defaultdict

class ThrottlingMiddleware(BaseMiddleware):
    """Rate limiting middleware - spam himoyasi"""
    
    def __init__(
        self,
        rate_limit: float = 0.5,  # sekundlar
        max_requests: int = 30,   # limit
        ban_time: int = 300       # ban vaqti (sekundlar)
    ):
        self.rate_limit = rate_limit
        self.max_requests = max_requests
        self.ban_time = ban_time
        self.users_data: Dict[int, Dict] = defaultdict(lambda: {
            'last_request': 0,
            'request_count': 0,
            'banned_until': 0
        })
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = data.get('event_from_user').id
        current_time = time.time()
        user_data = self.users_data[user_id]
        
        # Ban tekshirish
        if current_time < user_data['banned_until']:
            return None
        
        # Rate limit tekshirish
        if current_time - user_data['last_request'] < self.rate_limit:
            user_data['request_count'] += 1
            
            if user_data['request_count'] >= self.max_requests:
                user_data['banned_until'] = current_time + self.ban_time
                # Ogohlantirish xabarini yuborish
                return None
        else:
            user_data['request_count'] = 0
        
        user_data['last_request'] = current_time
        return await handler(event, data)
```

### 4. SQL Injection Himoyasi
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository:
    """Xavfsiz database operatsiyalari"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def search_products(
        self,
        query: str,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        limit: int = 20,
        offset: int = 0
    ) -> list[Product]:
        """Parametrlashtirilgan so'rovlar orqali xavfsiz qidiruv"""
        
        # HECH QACHON string interpolation ishlatmang!
        # ❌ XATO: f"SELECT * FROM products WHERE name LIKE '%{query}%'"
        
        # ✅ TO'G'RI: Parametrlashtirilgan so'rovlar
        stmt = select(Product).where(
            Product.is_active == True,
            Product.name.ilike(f'%{query}%')  # SQLAlchemy avtomat escape qiladi
        )
        
        if category_id:
            stmt = stmt.where(Product.category_id == category_id)
        
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
        
        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)
        
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
```

### 5. JWT Token Authentication
```python
import jwt
from datetime import datetime, timedelta
from typing import Optional

class JWTHandler:
    """JWT token boshqaruvi"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def create_access_token(
        self,
        user_id: int,
        role: str,
        expires_delta: timedelta = timedelta(hours=24)
    ) -> str:
        """Access token yaratish"""
        expire = datetime.utcnow() + expires_delta
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Token tekshirish"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
```

---

## 💳 TO'LOV INTEGRASIYASI

### Telegram Stars (Raqamli mahsulotlar uchun)
```python
from aiogram.types import LabeledPrice, Message
from aiogram.methods import CreateInvoiceLink

async def create_stars_invoice(
    bot: Bot,
    product: Product,
    user_id: int
) -> str:
    """Telegram Stars orqali to'lov havolasi yaratish"""
    
    prices = [
        LabeledPrice(
            label=product.name,
            amount=product.stars_price  # Stars miqdori
        )
    ]
    
    invoice_link = await bot.create_invoice_link(
        title=product.name,
        description=product.description[:255],
        payload=f"product_{product.id}_{user_id}",
        currency="XTR",  # Telegram Stars
        prices=prices,
        photo_url=product.image_url,
        photo_width=512,
        photo_height=512
    )
    
    return invoice_link
```

### Click/Payme (O'zbekiston) Integrasiyasi
```python
import hashlib
import aiohttp
from datetime import datetime

class PaymeIntegration:
    """Payme to'lov tizimi integratsiyasi"""
    
    def __init__(self, merchant_id: str, secret_key: str, test_mode: bool = True):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.base_url = "https://checkout.paycom.uz" if not test_mode else "https://test.paycom.uz"
    
    def generate_payment_url(
        self,
        order_id: str,
        amount: int,  # Tiyin (1 so'm = 100 tiyin)
        return_url: str
    ) -> str:
        """To'lov havolasi yaratish"""
        
        # Parametrlarni base64 formatda kodlash
        params = f"m={self.merchant_id};ac.order_id={order_id};a={amount};c={return_url}"
        encoded = base64.b64encode(params.encode()).decode()
        
        return f"{self.base_url}/{encoded}"
    
    async def verify_transaction(
        self,
        transaction_id: str,
        order_id: str,
        amount: int
    ) -> bool:
        """Tranzaksiyani tekshirish"""
        # API orqali tekshirish logikasi
        pass
```

---

## 🗄️ DATABASE MODELLARI

### User Model
```python
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    SELLER = "seller"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    first_name = Column(String(200), nullable=True)
    last_name = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    language = Column(String(5), default="uz")
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    # Xavfsizlik
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(Text, nullable=True)
    
    # Vaqtlar
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user", lazy="selectin")
    cart_items = relationship("CartItem", back_populates="user", lazy="selectin")
    reviews = relationship("Review", back_populates="user", lazy="selectin")
    seller_profile = relationship("Seller", back_populates="user", uselist=False)
```

### Product Model
```python
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    name = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    
    quantity = Column(Integer, default=0)
    sold_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    # Media
    images = Column(ARRAY(String), default=[])  # PostgreSQL array
    video_url = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    moderation_status = Column(Enum(ModerationStatus), default=ModerationStatus.PENDING)
    
    # SEO
    slug = Column(String(300), unique=True, index=True)
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(Text, nullable=True)
    
    # Analytics
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    seller = relationship("Seller", back_populates="products")
    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product", lazy="selectin")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
```

---

## 🎨 FOYDALANUVCHI INTERFEYSI

### Inline Keyboard yaratish
```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_product_keyboard(
    product_id: int,
    quantity: int,
    current_qty: int = 1,
    in_cart: bool = False
) -> InlineKeyboardMarkup:
    """Mahsulot uchun inline keyboard"""
    
    builder = InlineKeyboardBuilder()
    
    # Miqdor boshqaruvi
    builder.row(
        InlineKeyboardButton(
            text="➖",
            callback_data=f"qty:dec:{product_id}:{current_qty}"
        ),
        InlineKeyboardButton(
            text=f"📦 {current_qty} dona",
            callback_data="qty:show"
        ),
        InlineKeyboardButton(
            text="➕",
            callback_data=f"qty:inc:{product_id}:{current_qty}"
        )
    )
    
    # Savatga qo'shish
    if in_cart:
        builder.row(
            InlineKeyboardButton(
                text="✅ Savatda",
                callback_data=f"cart:view"
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="🛒 Savatga qo'shish",
                callback_data=f"cart:add:{product_id}:{current_qty}"
            )
        )
    
    # Qo'shimcha tugmalar
    builder.row(
        InlineKeyboardButton(
            text="❤️ Sevimli",
            callback_data=f"fav:add:{product_id}"
        ),
        InlineKeyboardButton(
            text="📝 Sharhlar",
            callback_data=f"reviews:{product_id}"
        )
    )
    
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Orqaga",
            callback_data="catalog:back"
        )
    )
    
    return builder.as_markup()
```

### Pagination
```python
from typing import Generic, TypeVar, List
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class PaginatedResult(Generic[T]):
    items: List[T]
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

def create_pagination_keyboard(
    current_page: int,
    total_pages: int,
    callback_prefix: str
) -> InlineKeyboardMarkup:
    """Pagination keyboard yaratish"""
    
    builder = InlineKeyboardBuilder()
    buttons = []
    
    # Birinchi sahifa
    if current_page > 2:
        buttons.append(
            InlineKeyboardButton(
                text="⏮️ 1",
                callback_data=f"{callback_prefix}:page:1"
            )
        )
    
    # Oldingi sahifa
    if current_page > 1:
        buttons.append(
            InlineKeyboardButton(
                text=f"◀️ {current_page - 1}",
                callback_data=f"{callback_prefix}:page:{current_page - 1}"
            )
        )
    
    # Joriy sahifa
    buttons.append(
        InlineKeyboardButton(
            text=f"· {current_page} ·",
            callback_data="page:current"
        )
    )
    
    # Keyingi sahifa
    if current_page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text=f"{current_page + 1} ▶️",
                callback_data=f"{callback_prefix}:page:{current_page + 1}"
            )
        )
    
    # Oxirgi sahifa
    if current_page < total_pages - 1:
        buttons.append(
            InlineKeyboardButton(
                text=f"{total_pages} ⏭️",
                callback_data=f"{callback_prefix}:page:{total_pages}"
            )
        )
    
    builder.row(*buttons)
    
    return builder.as_markup()
```

---

## 📊 FSM (Finite State Machine)

### Order States
```python
from aiogram.fsm.state import State, StatesGroup

class OrderStates(StatesGroup):
    """Buyurtma berish holatlari"""
    
    # Mahsulot tanlash
    selecting_products = State()
    viewing_product = State()
    
    # Savat
    cart_review = State()
    
    # Buyurtma ma'lumotlari
    entering_name = State()
    entering_phone = State()
    entering_address = State()
    selecting_delivery = State()
    
    # To'lov
    selecting_payment = State()
    processing_payment = State()
    
    # Tasdiqlash
    confirming_order = State()
    
    # Tugallangan
    order_completed = State()

class SellerStates(StatesGroup):
    """Sotuvchi holatlari"""
    
    # Ro'yxatdan o'tish
    registration_company = State()
    registration_phone = State()
    registration_address = State()
    registration_documents = State()
    
    # Mahsulot qo'shish
    adding_product_name = State()
    adding_product_description = State()
    adding_product_category = State()
    adding_product_price = State()
    adding_product_quantity = State()
    adding_product_images = State()
    adding_product_confirm = State()

class AdminStates(StatesGroup):
    """Admin holatlari"""
    
    # Xabar tarqatish
    broadcast_message = State()
    broadcast_confirm = State()
    
    # Foydalanuvchilarni boshqarish
    user_search = State()
    user_ban_reason = State()
    
    # Kategoriya boshqaruvi
    category_name = State()
    category_parent = State()
```

---

## 🔔 BILDIRISHNOMALAR

```python
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

class NotificationService:
    """Bildirishnomalar xizmati"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def notify_order_status(
        self,
        user_id: int,
        order_id: int,
        status: str,
        details: str = ""
    ):
        """Buyurtma holati haqida xabar"""
        
        status_emojis = {
            "pending": "⏳",
            "confirmed": "✅",
            "processing": "📦",
            "shipped": "🚚",
            "delivered": "🎉",
            "cancelled": "❌"
        }
        
        emoji = status_emojis.get(status, "📋")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📋 Buyurtmani ko'rish",
                callback_data=f"order:view:{order_id}"
            )]
        ])
        
        await self.bot.send_message(
            chat_id=user_id,
            text=f"{emoji} <b>Buyurtma #{order_id}</b>\n\n"
                 f"Holat: <b>{status}</b>\n"
                 f"{details}",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    
    async def notify_seller_new_order(
        self,
        seller_id: int,
        order: Order
    ):
        """Sotuvchiga yangi buyurtma haqida xabar"""
        
        await self.bot.send_message(
            chat_id=seller_id,
            text=f"🛒 <b>Yangi buyurtma!</b>\n\n"
                 f"Buyurtma: #{order.id}\n"
                 f"Mahsulotlar: {len(order.items)}\n"
                 f"Jami: {order.total_amount:,.0f} so'm\n\n"
                 f"Iltimos, buyurtmani qayta ishlang.",
            parse_mode="HTML"
        )
    
    async def broadcast(
        self,
        user_ids: List[int],
        message: str,
        keyboard: InlineKeyboardMarkup = None
    ) -> dict:
        """Ko'plab foydalanuvchilarga xabar tarqatish"""
        
        success = 0
        failed = 0
        
        for user_id in user_ids:
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
                success += 1
            except Exception:
                failed += 1
            
            # Rate limiting
            await asyncio.sleep(0.05)
        
        return {"success": success, "failed": failed}
```

---

## 🚀 ISHGA TUSHIRISH

### Docker Compose
```yaml
version: '3.8'

services:
  bot:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: china_market_bot
    restart: unless-stopped
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    networks:
      - bot_network
    volumes:
      - ./logs:/app/logs
      - ./media:/app/media

  postgres:
    image: postgres:15-alpine
    container_name: china_market_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - bot_network
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    container_name: china_market_redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - bot_network

  nginx:
    image: nginx:alpine
    container_name: china_market_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./media:/var/www/media
    depends_on:
      - bot
    networks:
      - bot_network

volumes:
  postgres_data:
  redis_data:

networks:
  bot_network:
    driver: bridge
```

### Environment Variables (.env.example)
```env
# Bot Configuration
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321

# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=china_market
DB_USER=postgres
DB_PASSWORD=your_secure_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Security
SECRET_KEY=your_super_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# Payment
PAYME_MERCHANT_ID=your_payme_merchant_id
PAYME_SECRET_KEY=your_payme_secret_key
CLICK_MERCHANT_ID=your_click_merchant_id
CLICK_SERVICE_ID=your_click_service_id
CLICK_SECRET_KEY=your_click_secret_key

# Media
MEDIA_PATH=/app/media
MAX_FILE_SIZE=10485760

# Logging
LOG_LEVEL=INFO
LOG_PATH=/app/logs
```

---

## 📈 TALAB QILINADIGAN FUNKSIYALAR

### Foydalanuvchi uchun:
1. ✅ Ro'yxatdan o'tish (telefon raqami bilan)
2. ✅ Mahsulotlar katalogi (kategoriyalar bo'yicha)
3. ✅ Mahsulotni qidirish (nom, kategoriya, narx bo'yicha)
4. ✅ Savatni boshqarish
5. ✅ Buyurtma berish
6. ✅ To'lov qilish (Telegram Stars, Click, Payme)
7. ✅ Buyurtmalar tarixi
8. ✅ Sevimli mahsulotlar
9. ✅ Sharhlar va baholash
10. ✅ Profil boshqaruvi
11. ✅ Bildirishnomalar
12. ✅ Ko'p tilli interfeys (UZ, RU, EN)

### Sotuvchi uchun:
1. ✅ Sotuvchi sifatida ro'yxatdan o'tish
2. ✅ Mahsulot qo'shish/tahrirlash/o'chirish
3. ✅ Buyurtmalarni boshqarish
4. ✅ Statistika va analitika
5. ✅ Daromad hisoboti
6. ✅ Mijozlar bilan muloqot

### Admin uchun:
1. ✅ Dashboard (statistika)
2. ✅ Foydalanuvchilarni boshqarish
3. ✅ Sotuvchilarni tasdiqlash/rad etish
4. ✅ Mahsulotlarni moderatsiya qilish
5. ✅ Kategoriyalarni boshqarish
6. ✅ Xabar tarqatish (broadcast)
7. ✅ Tizim sozlamalari
8. ✅ Hisobotlar

---

## ⚙️ QOIDALAR VA TALABLAR

1. **Barcha kod** async/await bilan yozilishi kerak
2. **Har bir handler** uchun alohida fayl yarating
3. **Type hints** ishlatish majburiy
4. **Docstrings** yozing
5. **Error handling** to'g'ri qiling
6. **Logging** ishlating
7. **Unit testlar** yozing
8. **PEP 8** standartlariga rioya qiling
9. **Security best practices** dan foydalaning
10. **Clean Code** tamoyillariga amal qiling

---

## 🎯 YAKUNIY NATIJA:

Professional, xavfsiz va to'liq funksiyali Telegram bozor botini yarating. Bot foydalanuvchilarga qulay interfeys, sotuvchilarga keng imkoniyatlar va adminlarga to'liq nazorat imkonini berishi kerak.

Kod sifati yuqori bo'lishi, hujjatlashtirilgan bo'lishi va oson kengaytiriladigan arxitekturaga ega bo'lishi kerak.
```

---

## 📝 QISQACHA XULOSA

Bu prompt quyidagilarni o'z ichiga oladi:

| Bo'lim | Tavsif |
|--------|--------|
| 🛠️ Texnologiyalar | aiogram 3.x, PostgreSQL, Redis, SQLAlchemy 2.0 |
| 📁 Struktura | Modular, kengaytiriladigan arxitektura |
| 🔐 Xavfsizlik | Shifrlash, Rate Limiting, Input Validation, JWT |
| 💳 To'lov | Telegram Stars, Click, Payme integratsiyasi |
| 🗄️ Database | To'liq modellashtirilgan ERD |
| 🎨 UI/UX | Zamonaviy inline klaviaturalar |
| 📊 FSM | Murakkab holatlar boshqaruvi |
| 🚀 Deploy | Docker Compose tayyor konfiguratsiya |

---

*Yaratildi: 2026-yil | Versiya: 1.0.0*
*Professional Telegram Bot Development Prompt for Claude Opus AI*
