from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False
    APP_NAME: str = "Task Manager"
    APP_VERSION: str = "1.0.1"

    class Config:
        env_file = ".env"

settings = Settings()
