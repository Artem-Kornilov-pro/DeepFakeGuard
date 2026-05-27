"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = "postgresql+asyncpg://deepfake:deepfake@localhost:5432/deepfakeguard"
    database_url_sync: str = "postgresql+psycopg2://deepfake:deepfake@localhost:5432/deepfakeguard"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me-to-a-random-secret-key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "videos"
    minio_secure: bool = False
    debug: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return cached Settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
