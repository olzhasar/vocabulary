from jose import jwt

from api.utils import generate_access_token
from config.settings import settings


def test_generate_access_token():
    data = {"email": "info@example.com"}

    token = generate_access_token(data)

    assert token

    decoded = jwt.decode(token, settings.SECRET_KEY)

    assert decoded["email"] == data["email"]
    assert "exp" in decoded
