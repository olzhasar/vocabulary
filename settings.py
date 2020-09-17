from pydantic import BaseSettings
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    TESTING: bool = False

    DB_DRIVER: str = "postgresql"
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_DATABASE: str = "vocabulary"

    DB_DSN = URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    )

    DB_POOL_MIN_SIZE: int = 1
    DB_POOL_MAX_SIZE: int = 16
    DB_ECHO: bool = False
    DB_USE_CONNECTION_FOR_REQUEST: bool = True
    DB_RETRY_LIMIT: int = 1
    DB_RETRY_INTERVAL: int = 1

    WORDS_API_KEY: str


settings = Settings(_env_file=".env")
