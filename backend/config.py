from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import os
from dotenv import load_dotenv
import secrets
from datetime import timedelta

load_dotenv()

class Settings(BaseSettings):
    # LM Studio Settings
    LM_STUDIO_URL: str = "http://localhost:1234/v1"
    LM_STUDIO_MAX_TOKENS: int = 800
    LM_STUDIO_TEMPERATURE: float = 0.7
    
    # Web Retrieval Settings
    CACHE_DIR: str = "cache"
    CACHE_DURATION: int = 3600  # Cache duration in seconds
    MAX_SEARCH_RESULTS: int = 5
    
    # Conversation Settings
    MAX_CONVERSATION_HISTORY: int = 10
    CONVERSATION_EXPIRY: int = 3600  # Conversation expiry in seconds
    
    # Database Settings
    DATABASE_URL: Optional[str] = None
    
    # Authentication Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_MIN_LENGTH: int = 8
    
    # Tag Settings
    MAX_TAGS_PER_CONVERSATION: int = 10
    MAX_TAG_LENGTH: int = 50
    
    # Category Settings
    MAX_CATEGORIES_PER_USER: int = 20
    MAX_CATEGORY_NAME_LENGTH: int = 100
    
    # Sharing Settings
    SHARE_INVITE_EXPIRY: timedelta = timedelta(days=7)
    MAX_SHARED_CONVERSATIONS: int = 50
    MAX_PENDING_INVITES: int = 20
    
    # Analytics Settings
    ANALYTICS_RETENTION_DAYS: int = 90
    ANALYTICS_UPDATE_INTERVAL: int = 3600  # Update interval in seconds
    MAX_ANALYTICS_POINTS: int = 1000  # Maximum number of data points for time series
    
    # LLM Settings
    LM_STUDIO_URL: str = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
    MAX_CONVERSATION_HISTORY: int = os.getenv("MAX_CONVERSATION_HISTORY", 10)
    CONVERSATION_EXPIRY: int = os.getenv("CONVERSATION_EXPIRY", 3600)
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./analytics.db")
    
    # Authentication Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secure-secret-key")
    API_KEY_EXPIRY_DAYS: int = os.getenv("API_KEY_EXPIRY_DAYS", 30)
    
    # Analytics Settings
    ANALYTICS_CLEANUP_DAYS: int = os.getenv("ANALYTICS_CLEANUP_DAYS", 30)
    ENABLE_ADVANCED_ANALYTICS: bool = os.getenv("ENABLE_ADVANCED_ANALYTICS", True)
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = os.getenv("PORT", 8000)
    DEBUG: bool = os.getenv("DEBUG", True)
    
    # Cache Settings
    CACHE_DIR: str = os.getenv("CACHE_DIR", os.path.join(os.path.dirname(__file__), "cache"))
    CACHE_EXPIRY: int = os.getenv("CACHE_EXPIRY", 3600)  # 1 hour in seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Create cache directory if it doesn't exist
os.makedirs(get_settings().CACHE_DIR, exist_ok=True)
