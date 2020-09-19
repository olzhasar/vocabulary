import pytest

from db.models import User
from db.tests.factories import UserFactory


@pytest.mark.asyncio
async def test_login(client, use_db):
    await UserFactory(email="vincent@vega.com", password="pulpfiction")

    response = await client.post(
        "/token", data=dict(username="vincent@vega.com", password="pulpfiction")
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_signup(client, use_db):
    response = await client.post(
        "/signup",
        json=dict(
            email="vincent@vega.com",
            password="pulpfiction",
            repeat_password="pulpfiction",
        ),
    )

    assert response.status_code == 201

    user_from_db = await User.query.where(
        User.email == "vincent@vega.com"
    ).gino.first()

    assert user_from_db
    assert user_from_db.check_password("pulpfiction")
