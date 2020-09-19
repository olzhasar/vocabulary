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
    async def test_register_without_password(self, use_db):
        user = await User.register(email="info@example.com")
        assert user
        assert isinstance(user, User)

        user_from_db = await User.query.where(
            User.email == "info@example.com"
        ).gino.first()

        assert user_from_db.id == user.id

    @pytest.mark.asyncio
    async def test_register_with_password(self, use_db):
        await User.register(email="info@example.com", password="123qweasd")

        user_from_db = await User.query.where(
            User.email == "info@example.com"
        ).gino.first()
        assert user_from_db.check_password("123qweasd")

    @pytest.mark.asyncio
    async def test_check_password(self, use_db):
        user = await User.register(email="info@example.com")

        assert not user.check_password("")
        assert not user.check_password("random string")

        user2 = await User.register(
            email="info@example2.com", password="123qweasd"
        )

        assert user2.check_password("123qweasd")
        assert not user2.check_password("")
        assert not user2.check_password("random string")

    @pytest.mark.asyncio
    async def test_authenticate(self, use_db):
        await User.register(email="info@example.com", password="123qweasd")

        assert not await User.authenticate("info@example.com", "WrongPassword")
        assert not await User.authenticate("wrong@email.com", "123qweasd")
        user = await User.authenticate("info@example.com", "123qweasd")

        assert user
        assert user.email == "info@example.com"
