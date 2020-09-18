import pytest

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
