"""Settings management.

Reads variables from .env and environment. All fields have defaults so
the app boots without a .env file during development and testing.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "refinery"
    app_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    debug: bool = False
    port: int = 8000


@lru_cache
def get_settings() -> Settings:
    """Return the cached Settings instance."""
    return Settings()
