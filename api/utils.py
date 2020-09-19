from datetime import datetime, timedelta

from jose import jwt

from config.settings import settings


def generate_access_token(data: dict) -> str:
    payload = data.copy()
    expiration = datetime.now() + timedelta(
        minutes=settings.JWT_LIFETIME_MINUTES
    )

    payload.update({"exp": expiration})
    return jwt.encode(payload, settings.SECRET_KEY)
