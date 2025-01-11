from functools import lru_cache

from pydantic import PostgresDsn
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

    postgres_server: str = "db"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"

    @property
    def database_uri(self) -> str:
        dsn = PostgresDsn.build(
            scheme="postgresql+psycopg",
            host=self.postgres_server,
            port=self.postgres_port,
            username=self.postgres_user,
            password=self.postgres_password,
            path=self.postgres_db or "",
        )
        return str(dsn)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
