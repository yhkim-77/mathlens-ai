from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "MathLens AI API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./mathlens.db"

    # JWT
    SECRET_KEY: str = "change-me-in-production-use-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"

    # Anthropic (backup)
    ANTHROPIC_API_KEY: Optional[str] = None

    # MathPix
    MATHPIX_APP_ID: Optional[str] = None
    MATHPIX_APP_KEY: Optional[str] = None

    # Redis (optional async queue)
    REDIS_URL: Optional[str] = None

    # Submission limits
    MAX_IMAGE_BYTES_BASE64: int = 2_800_000   # ~2 MB decoded
    MAX_IMAGE_UPLOAD_BYTES: int = 2_097_152   # 2 MB raw

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
