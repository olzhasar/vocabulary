import pytest

from db import db
from users.models import User, users


@pytest.mark.asyncio
class TestUser:
    async def test_create_get(self, use_db):
        user_id = await User.create(email="info@test.com", password="123qweasd")
        assert user_id

        query = users.count()
        assert await db.execute(query) == 1

        user = await User.get(id=user_id)
        assert user["id"] == user_id
        assert user["email"] == "info@test.com"

        user2 = await User.get(email="info@test.com")
        assert user == user2
