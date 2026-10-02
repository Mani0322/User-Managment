from pydantic_settings import BaseSettings,SettingsConfigDict

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
    DATABASE_URL="mysql+pymysql://root:your_mysql_password@localhost:3306/user_management_db"

    #CORS Settings
    CORS_ORGINS:list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()