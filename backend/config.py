"""
Application configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/microscope_db"

    # Raspberry Pi
    RPI_URL: str = "http://raspberrypi.local:5000"
    RPI_TIMEOUT: int = 10

    # Storage
    IMAGES_PATH: str = "./images"
    THUMBNAILS_PATH: str = "./thumbnails"
    THUMBNAIL_SIZE: int = 400

    # Camera
    CAMERA_INDEX: int = 0

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Safety Limits (steps)
    MAX_X_POSITION: float = 10000.0
    MAX_Y_POSITION: float = 10000.0
    MAX_Z_POSITION: float = 5000.0
    MIN_X_POSITION: float = 0.0
    MIN_Y_POSITION: float = 0.0
    MIN_Z_POSITION: float = 0.0

    # Watchdog
    WATCHDOG_TIMEOUT: int = 30

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:8000"

    # Application
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    This ensures we only load the settings once.
    """
    return Settings()
