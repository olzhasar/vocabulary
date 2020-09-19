import pytest
from httpx import AsyncClient

from config.settings import DB_DSN, settings

settings.TESTING = True


@pytest.fixture
async def use_db():
    from db import db

    await db.set_bind(DB_DSN)
    await db.gino.create_all()

    yield

    await db.gino.drop_all()
    await db.pop_bind().close()


@pytest.fixture
async def client():
    from api.main import app

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client
