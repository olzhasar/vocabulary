import pytest

from db.tests.factories import UserFactory


@pytest.mark.asyncio
async def test_login(client, use_db):
    await UserFactory(email="vincent@vega.com", password="pulpfiction")

    response = await client.post(
        "/token", data=dict(username="vincent@vega.com", password="pulpfiction")
    )

    assert response.status_code == 200
