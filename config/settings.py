"""Configuração central via variáveis de ambiente / arquivo .env."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do framework (Restful Booker Platform)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    base_url: str = "https://automationintesting.online"
    api_url: str = "https://automationintesting.online/api"
    admin_user: str = "admin"
    admin_password: str = "password"


@lru_cache
def get_settings() -> Settings:
    """Retorna a instância única (cacheada) das configurações."""
    return Settings()
