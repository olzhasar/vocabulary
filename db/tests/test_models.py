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
        await User.create(id=1, email="info@example.com")

        assert await User.get(1)

        user_from_db = await User.query.where(
            User.email == "info@example.com"
        ).gino.first()

        assert user_from_db.id == 1
        assert user_from_db.email == "info@example.com"

    @pytest.mark.asyncio
    async def test_password_set_check(self, use_db):
        user = await User.create(id=1, email="info@example.com")

        assert not user.password_hash

        user.set_password("123qweasd")
        assert user.password_hash

        assert user.check_password("123qweasd")
        assert not user.check_password("WrongPassword")
