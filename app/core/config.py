from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Auth Backend"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "auth_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def get_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SQLALCHEMY_DATABASE_URI = self.get_database_url

    # JWT
    SECRET_KEY: str = (
        "your-secret-key"  # Replace with a secure random key in production
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10

    # Password Policy
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_SPECIAL_CHAR: bool = True
    REQUIRE_NUMBER: bool = True
    REQUIRE_UPPERCASE: bool = True

    # Session
    SESSION_EXPIRE_DAYS: int = 30

    # 2FA
    ENABLE_2FA: bool = False

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",  # Allow extra fields without raising validation errors
    )


settings = Settings()
