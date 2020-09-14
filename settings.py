from pydantic import BaseSettings


class Settings(BaseSettings):
    TESTING: bool = False

    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/vocabulary"
    TEST_DATABASE_URL: str = (
        "postgresql://vocabulary:vocabulary@localhost:5432/vocabulary_test"
    )

    WORDS_API_KEY: str


settings = Settings(_env_file=".env")
