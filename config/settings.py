import os

from pydantic import BaseSettings
from sqlalchemy.engine.url import URL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    TESTING: bool = False

    SECRET_KEY: str = "VOCABULARY_SECRET"
    JWT_LIFETIME_MINUTES: int = 60 * 24

    DB_DRIVER: str = "postgresql"
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    DB_DATABASE: str = "vocabulary"
    DB_TEST_DATABASE: str = "vocabulary_test"

    DB_POOL_MIN_SIZE: int = 1
    DB_POOL_MAX_SIZE: int = 16
    DB_ECHO: bool = False
    DB_USE_CONNECTION_FOR_REQUEST: bool = True
    DB_RETRY_LIMIT: int = 1
    DB_RETRY_INTERVAL: int = 1

    WORDS_API_KEY: str


settings = Settings(_env_file=os.path.join(BASE_DIR, ".env"))

DB_DATABASE = (
    settings.DB_TEST_DATABASE if settings.TESTING else settings.DB_DATABASE
)
DB_DSN = URL(
    drivername=settings.DB_DRIVER,
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=DB_DATABASE,
)
