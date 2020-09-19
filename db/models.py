from typing import Optional

import bcrypt

from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(100))

    email_verified = db.Column(db.Boolean, default=False)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def check_password(self, password: str) -> bool:
        if self.password_hash:
            return bcrypt.checkpw(
                password.encode("utf-8"), self.password_hash.encode("utf-8")
            )
        return False

    @classmethod
    async def register(
        cls, email: str, password: Optional[str] = None, **kwargs
    ):
        password_hash = cls.hash_password(password) if password else None
        return await cls.create(
            email=email, password_hash=password_hash, **kwargs
        )

    @classmethod
    async def authenticate(cls, email: str, password: str):
        user = await cls.query.where(cls.email == email).gino.first()
        if not user:
            return False

        return user.check_password(password)
