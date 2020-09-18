import pytest

from db.models import User


class TestUser:
    @pytest.mark.parametrize(
        "password", ["Password", "123qweasd", "QWERTY~!@#$%^"]
    )
    def test_hash_password(self, password):
        hashed = User.hash_password(password)
        assert hashed
        assert hashed != password

    @pytest.mark.asyncio
    async def test_create(self, use_db):
        await User.create(
            id=1, email="info@example.com", password_hash="123qweasd"
        )

        assert await User.get(1)

        user_from_db = await User.query.where(
            User.email == "info@example.com"
        ).gino.first()

        assert user_from_db.id == 1
        assert user_from_db.email == "info@example.com"
