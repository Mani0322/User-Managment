from pydantic_settings import BaseSettings,SettingsConfigDict
from urllib.parse import quote_plus



class Settings(BaseSettings):
    # App settings
    PROJECT_NAME: str = "User Management Microservice"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Secrets: NO value here, must come from .env
    SECRET_KEY: str
    DATABASE_URL: str
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Normal settings: safe to keep defaults
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: list[str] = ["*"]
    REDIS_URL: str = "redis://localhost:6379/0"
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    EMAIL_FROM: str = "noreply@user-management.local"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()