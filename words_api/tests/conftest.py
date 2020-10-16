import pytest


@pytest.fixture(autouse=True)
async def words_api_session():
    from words_api.client import words_api_client

    words_api_client.setup_session()

    yield

    await words_api_client.close_session()
