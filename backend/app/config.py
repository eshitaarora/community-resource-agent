import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    # App
    APP_NAME: str = "Community Resource Navigation AI"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///community_resources.db"
    
    # AI/LLM - Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3-flash-preview"
    
    # Services
    GOOGLE_MAPS_API_KEY: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE: str = ""
    
    # Cache
    REDIS_URL: str = "redis://redis:6379/0"
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]


settings = Settings()

