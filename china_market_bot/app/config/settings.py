"""
⚙️ Configuration Settings Module

Pydantic Settings for environment variables management.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings are loaded from .env file or environment variables.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ==========================================
    # Bot Configuration
    # ==========================================
    bot_token: str = Field(..., description="Telegram Bot Token from @BotFather")
    admin_ids: List[int] = Field(default_factory=list, description="List of admin Telegram IDs")
    bot_username: str = Field(default="china_market_bot", description="Bot username")
    
    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        """Parse admin IDs from comma-separated string."""
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v or []
    
    # ==========================================
    # Database Configuration
    # ==========================================
    db_host: str = Field(default="localhost", description="PostgreSQL host")
    db_port: int = Field(default=5432, description="PostgreSQL port")
    db_name: str = Field(default="china_market", description="Database name")
    db_user: str = Field(default="postgres", description="Database user")
    db_password: str = Field(default="", description="Database password")
    
    @property
    def database_url(self) -> str:
        """Get async database URL."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    @property
    def database_url_sync(self) -> str:
        """Get sync database URL for Alembic."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    # ==========================================
    # Redis Configuration
    # ==========================================
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")
    redis_password: Optional[str] = Field(default=None, description="Redis password")
    
    @property
    def redis_url(self) -> str:
        """Get Redis URL."""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # ==========================================
    # Security Configuration
    # ==========================================
    secret_key: str = Field(
        default="change_me_in_production_32_chars",
        min_length=32,
        description="Secret key for JWT and encryption"
    )
    encryption_key: Optional[str] = Field(
        default=None,
        description="Fernet encryption key"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_hours: int = Field(default=24, description="Access token expiration hours")
    
    # ==========================================
    # Payment Configuration
    # ==========================================
    telegram_stars_enabled: bool = Field(default=True, description="Enable Telegram Stars payment")
    
    # Payme
    payme_merchant_id: Optional[str] = Field(default=None, description="Payme merchant ID")
    payme_secret_key: Optional[str] = Field(default=None, description="Payme secret key")
    payme_test_mode: bool = Field(default=True, description="Payme test mode")
    
    # Click
    click_merchant_id: Optional[str] = Field(default=None, description="Click merchant ID")
    click_service_id: Optional[str] = Field(default=None, description="Click service ID")
    click_secret_key: Optional[str] = Field(default=None, description="Click secret key")
    click_test_mode: bool = Field(default=True, description="Click test mode")
    
    # ==========================================
    # Media Configuration
    # ==========================================
    media_path: str = Field(default="./media", description="Media storage path")
    max_file_size: int = Field(default=10485760, description="Max file size in bytes (10MB)")
    allowed_extensions: List[str] = Field(
        default_factory=lambda: ["jpg", "jpeg", "png", "gif", "webp"],
        description="Allowed file extensions"
    )
    
    @field_validator("allowed_extensions", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        """Parse extensions from comma-separated string."""
        if isinstance(v, str):
            return [x.strip().lower() for x in v.split(",") if x.strip()]
        return v or []
    
    # ==========================================
    # Logging Configuration
    # ==========================================
    log_level: str = Field(default="INFO", description="Logging level")
    log_path: str = Field(default="./logs", description="Log files path")
    log_format: str = Field(default="json", description="Log format (json/text)")
    
    # ==========================================
    # Rate Limiting Configuration
    # ==========================================
    rate_limit_requests: int = Field(default=30, description="Max requests per period")
    rate_limit_period: int = Field(default=60, description="Rate limit period in seconds")
    ban_time_seconds: int = Field(default=300, description="Ban time in seconds")
    
    # ==========================================
    # Localization Configuration
    # ==========================================
    default_language: str = Field(default="uz", description="Default language")
    supported_languages: List[str] = Field(
        default_factory=lambda: ["uz", "ru", "en"],
        description="Supported languages"
    )
    
    @field_validator("supported_languages", mode="before")
    @classmethod
    def parse_languages(cls, v):
        """Parse languages from comma-separated string."""
        if isinstance(v, str):
            return [x.strip().lower() for x in v.split(",") if x.strip()]
        return v or []
    
    # ==========================================
    # Webhook Configuration
    # ==========================================
    webhook_host: Optional[str] = Field(default=None, description="Webhook host URL")
    webhook_path: str = Field(default="/webhook", description="Webhook path")
    webhook_port: int = Field(default=8443, description="Webhook port")
    use_webhook: bool = Field(default=False, description="Use webhook instead of polling")
    
    # ==========================================
    # Development Configuration
    # ==========================================
    debug: bool = Field(default=False, description="Debug mode")


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are loaded only once.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()
