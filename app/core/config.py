"""Application configuration."""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = Field(default="DataPulse", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    database_url: str = Field(default="sqlite:///./datapulse.db", alias="DATABASE_URL")
    auth_enabled: bool = Field(default=False, alias="AUTH_ENABLED")
    jwt_secret_key: str = Field(default="change-me-in-production", alias="JWT_SECRET_KEY")
    jwt_access_token_minutes: int = Field(default=30, alias="JWT_ACCESS_TOKEN_MINUTES")
    jwt_refresh_token_minutes: int = Field(default=60 * 24 * 7, alias="JWT_REFRESH_TOKEN_MINUTES")
    cors_origins: list[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"],
        alias="CORS_ORIGINS",
    )
    airflow_base_url: str | None = Field(default=None, alias="AIRFLOW_BASE_URL")
    airflow_mock_mode: bool = Field(default=True, alias="AIRFLOW_MOCK_MODE")
    rate_limit_requests: int = Field(default=120, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return cached settings so dependencies can share one config object."""
    return Settings()


settings = get_settings()
