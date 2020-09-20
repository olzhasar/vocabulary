import pytest

from api.auth import generate_access_token
from db.models import User
from db.tests.factories import UserFactory


@pytest.mark.asyncio
async def test_login(client, use_db):
    await UserFactory(email="vincent@vega.com", password="pulpfiction")

    response = await client.post(
        "/token", data=dict(username="vincent@vega.com", password="pulpfiction")
    )

    assert response.status_code == 200

    response_json = response.json()
    assert "access_token" in response_json
    assert "token_type" in response_json


@pytest.mark.asyncio
async def test_bad_login(client, use_db):
    await UserFactory(email="vincent@vega.com", password="pulpfiction")

    response = await client.post(
        "/token",
        data=dict(username="vincent@vega.com", password="wrongpassword"),
    )

    assert response.status_code == 422


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


@pytest.mark.asyncio
async def test_signup_email_in_use(client, use_db):
    await UserFactory(email="vincent@vega.com")

    response = await client.post(
        "/signup",
        json=dict(
            email="vincent@vega.com",
            password="pulpfiction",
            repeat_password="pulpfiction",
        ),
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_word_list_unauthenticated(client, use_db):
    response = await client.get("/words")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_word_list_ok(client, use_db):
    user = await UserFactory(email="vincent@vega.com")
    token = generate_access_token(user.email)
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/words", headers=headers)
    assert response.status_code == 200
