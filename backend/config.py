from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_PASSWORD: str
    DB_HOST: str
    DB_USER: str
    DB_NAME: str
    DB_PORT: int
    SECRET_KEY: str
    SERVER_HOST: str
    EMAIL_TEMPLATES_DIR: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str

    # store the values in .env file
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
