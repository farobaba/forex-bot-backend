from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path


class Settings(BaseSettings):
    # API Configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_TITLE: str = "Exness AI Trading Bot API"
    API_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/forex_bot_db"
    DATABASE_ECHO: bool = True
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Exness MT5
    EXNESS_LOGIN: str = "your_exness_login"
    EXNESS_PASSWORD: str = "your_exness_password"
    EXNESS_SERVER: str = "ExnessFXPro"
    
    # Trading
    TARGET_SYMBOL: str = "XAUUSD"
    TARGET_TIMEFRAME: int = 5
    RISK_PER_TRADE: float = 2.0
    MAX_DAILY_LOSS: float = 5.0
    MAX_DRAWDOWN: float = 10.0
    SIGNAL_CONFIDENCE_THRESHOLD: int = 70
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
