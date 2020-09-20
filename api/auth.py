from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.settings import settings
from db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def generate_access_token(
    email: str, expiration: Optional[datetime] = None, **kwargs
) -> str:
    expiration = expiration or datetime.now() + timedelta(
        minutes=settings.JWT_LIFETIME_MINUTES
    )
    payload = dict(email=email, exp=expiration, **kwargs)

    return jwt.encode(payload, settings.SECRET_KEY)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        email = payload.get("email")
        if email is None:
            raise invalid_credentials
        expiration = payload.get("exp")
        if (
            not expiration
            or datetime.fromtimestamp(expiration) < datetime.now()
        ):
            raise invalid_credentials
    except JWTError:
        raise invalid_credentials

    user = await User.get_by_email(email)
    if not user:
        raise invalid_credentials

    return user
