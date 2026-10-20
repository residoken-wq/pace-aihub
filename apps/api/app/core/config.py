from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings from env only. Secrets are SecretStr so they never render in logs."""

    model_config = SettingsConfigDict(env_prefix="PACE_", extra="ignore")

    env: Literal["dev", "test", "pilot"] = "dev"
    log_level: str = "INFO"
    database_url: SecretStr = Field(
        description="SQLAlchemy async URL, e.g. postgresql+asyncpg://user:pass@host/db"
    )
    valkey_url: SecretStr = Field(description="Redis-protocol URL of the Valkey instance")
    readiness_timeout_s: float = 2.0


@lru_cache
def get_settings() -> Settings:
    return Settings()  # values come from env
