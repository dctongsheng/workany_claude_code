"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_prefix="WORKANY_", env_file=".env", extra="ignore")

    # Application
    debug: bool = False
    app_name: str = "WorkAny API"

    # Server ports
    api_port_dev: int = 3026
    api_port_prod: int = 2620

    # Node.js service (for AI/Sandbox proxy)
    node_service_url: str = "http://localhost:2026"

    # Database
    database_url: str = "sqlite+aiosqlite:///./workany.db"

    # CORS
    cors_origins: list[str] = ["*"]

    @property
    def api_port(self) -> int:
        """Get the API port based on debug mode."""
        return self.api_port_dev if self.debug else self.api_port_prod


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
