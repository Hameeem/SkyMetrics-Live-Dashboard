import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "SkyMetrics"
    APP_ENV: str = "development"
    SECRET_KEY: str = "skymetrics-secret-key-super-secure-production-ready-2026"
    DEBUG: bool = True

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_API_URL: str = "http://localhost:8000"

    DATABASE_URL: str = "sqlite:///./skymetrics.db"

    OPENSKY_USERNAME: Optional[str] = None
    OPENSKY_PASSWORD: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None

    MODEL_PATH: str = "ml/artifacts/delay_model.joblib"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
