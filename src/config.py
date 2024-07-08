from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated
from fastapi import Depends
from functools import lru_cache


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


@lru_cache
def get_settings_service() -> Settings:
    return Settings()


settings = Settings()
SettingsService = Annotated[Settings, Depends(get_settings_service)]
