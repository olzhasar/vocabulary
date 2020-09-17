import pytest

from users.models import User


@pytest.mark.asyncio
class TestUser:
    @pytest.mark.parametrize(
        "password", ["Password", "123qweasd", "QWERTY~!@#$%^"]
    )
    def test_hash_password(self, password):
        hashed = User.hash_password(password)
        assert hashed
        assert hashed != password

    async def test_create(self, use_db):
        user = await User.objects.create(
            id=1, email="info@example.com", password_hash="123qweasd"
        )

        user = await user.load()

        user_from_db = await User.get(email="info@example.com")

        assert user_from_db.id == 1
