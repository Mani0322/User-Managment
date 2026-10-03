from pydantic_settings import BaseSettings,SettingsConfigDict
from urllib.parse import quote_plus



password = quote_plus("beinex@app")

class Settings(BaseSettings):
    # App settings
    PROJECT_NAME:str = "User Management Microservice"
    VERSION:str = "1.0.0"
    DEBUG:bool = True

    # security settings
    SECRET_KEY:str = "af91a3ef1c47990aeaf736a7a4b4faec1ca21cbbb9a1c3c9a8dd062e7f4d2cc5"
    ALGORITHM:str= "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30

    # Database Settings
    DATABASE_URL:str=f"mysql+pymysql://root:{password}@localhost:3306/micro_db"

    #CORS Settings
    CORS_ORGINS:list[str] = ["*"]

     # Celery / Redis Settings
    REDIS_URL: str = "redis://localhost:6379/0"

    # Email Settings
    SMTP_HOST: str = "sandbox.smtp.mailtrap.io"
    SMTP_PORT: int = 2525
    SMTP_USER: str = "70a43966e302ed"
    SMTP_PASSWORD: str = "b12af16ec5c683"
    EMAIL_FROM: str = "noreply@user-management.local"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()