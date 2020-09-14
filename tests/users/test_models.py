import pytest

from users.models import User


@pytest.mark.asyncio
class TestUser:
    async def test_create(self, use_db):
        user_id = await User.create(email="info@test.com", password="123qweasd")
        assert user_id

        assert User.get(user_id)
