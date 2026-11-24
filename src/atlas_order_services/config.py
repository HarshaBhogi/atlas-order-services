from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ATLAS_", extra="ignore")

    app_name: str = "Atlas Order Services"
    environment: str = "local"
    database_url: str = "sqlite+pysqlite:///./data/atlas.db"
    document_root: Path = Field(default=Path("./documents"))
    log_level: str = "INFO"
    page_size_default: int = 20
    page_size_max: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()
