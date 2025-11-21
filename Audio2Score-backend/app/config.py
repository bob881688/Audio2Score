"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/audio2score"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days
    
    # Server
    port: int = 8000
    node_env: str = "development"
    
    # CORS
    allowed_origins: str = "*"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
