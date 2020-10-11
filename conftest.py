import pytest
from httpx import AsyncClient

from api.auth import generate_access_token
from config.settings import settings
from db.tests.factories import UserFactory

settings.TESTING = True


@pytest.fixture
async def use_db():
    from config.settings import get_db_dsn
    from db import db

    DB_DSN = get_db_dsn()

    async with db.with_bind(DB_DSN):
        await db.gino.create_all()

        yield

        await db.gino.drop_all()


@pytest.fixture
async def client():
    from api.main import app

    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture
async def auth_client():
    from api.main import app

    user = await UserFactory()

    token = generate_access_token(user.email)
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(
        app=app, base_url="http://localhost:8000", headers=headers
    ) as client:
        yield client
