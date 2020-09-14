import pytest

from settings import settings

settings.DATABASE_URL = settings.TEST_DATABASE_URL


@pytest.fixture(scope="session")
def monkeysession(request):
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture
async def use_db():
    from db import db, metadata

    metadata.bind = settings.TEST_DATABASE_URL
    metadata.create_all()

    async with db:
        yield

    metadata.drop_all()
