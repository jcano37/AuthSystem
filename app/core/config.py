from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def get_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SQLALCHEMY_DATABASE_URI = self.get_database_url

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: Optional[str] = None

    # Email
    SMTP_TLS: bool
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # CORS
    BACKEND_CORS_ORIGINS: list

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int

    # Password Policy
    MIN_PASSWORD_LENGTH: int
    REQUIRE_SPECIAL_CHAR: bool
    REQUIRE_NUMBER: bool
    REQUIRE_UPPERCASE: bool

    # Session
    SESSION_EXPIRE_DAYS: int

    # 2FA
    ENABLE_2FA: bool

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = 'ignore'  # Allow extra fields without raising validation errors


settings = Settings()
