from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql://localhost:5432/remcostoeten"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # API
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"

    # Feature flags
    ENABLE_ANALYTICS: bool = True
    ENABLE_FEEDBACK: bool = True
    INCREMENT_VIEWS_ONLY_IN_PRODUCTION: bool = True

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://remcostoeten.nl",
        "https://www.remcostoeten.nl"
    ]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Global settings instance
settings = get_settings()