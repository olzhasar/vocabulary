from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from api.auth import generate_access_token, get_current_user
from config.settings import settings
from db.tests.factories import UserFactory


def test_generate_access_token():
    email = "info@example.com"

    token = generate_access_token(email)

    assert token

    decoded = jwt.decode(token, settings.SECRET_KEY)

    assert decoded["email"] == email
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_get_current_user(use_db):
    user = await UserFactory(email="vincent@vega.com")
    token = generate_access_token(user.email)

    user_from_token = await get_current_user(token)

    assert user_from_token.id == user.id


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(use_db):
    await UserFactory(email="vincent@vega.com")
    token = generate_access_token("info@example.com")

    with pytest.raises(HTTPException):
        await get_current_user(token)


@pytest.mark.asyncio
async def test_get_current_user_expired_token(use_db):
    user = await UserFactory(email="vincent@vega.com")
    expiration = datetime.now() - timedelta(
        minutes=settings.JWT_LIFETIME_MINUTES + 1
    )
    token = generate_access_token(user.email, expiration=expiration)

    with pytest.raises(HTTPException):
        await get_current_user(token)
