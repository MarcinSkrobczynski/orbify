from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSettings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, case_sensitive=True, env_prefix="CORS_", extra="ignore")

    allow_origins: list[str] | None = None
    allow_credentials: bool = True
    allow_methods: list[str] | None = None
    allow_headers: list[str] | None = None
    max_age: int = 3600


class Settings(BaseSettings):
    debug: bool = False

    project_name: str = "orbify_projects"
    version: str = "0.1.0"
    api_prefix: str = "/api"

    cors_settings: CORSSettings = CORSSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
