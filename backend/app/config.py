"""
Configuration management for the application.
Loads environment variables and provides configuration settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/pharma_complaint_db"
    
    # JWT Authentication
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Groq API
    groq_api_key: str = ""
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload
    max_file_size: int = 10485760  # 10MB in bytes
    upload_dir: str = "./uploads"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
