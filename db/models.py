from typing import Optional

import bcrypt
from asyncpg.exceptions import UniqueViolationError

from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
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
    async def get_by_email(cls, email: str):
        return await cls.query.where(cls.email == email).gino.first()

    @classmethod
    async def register(
        cls, email: str, password: Optional[str] = None, **kwargs
    ):
        password_hash = cls.hash_password(password) if password else None
        return await cls.create(
            email=email, password_hash=password_hash, **kwargs
        )

    @classmethod
    async def authenticate(cls, username: str, password: str):
        user = await cls.query.where(cls.email == username).gino.first()
        if not user:
            return False

        if not user.check_password(password):
            return False

        return user


class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)

    description = db.Column(db.JSON())

    @classmethod
    async def get_or_create(cls, name: str):
        name = name.lower()
        try:
            word = await cls.create(name=name)
        except UniqueViolationError:
            word = await cls.query.where(cls.name == name).gino.first()
            created = False
        else:
            created = True
        return word, created


class UserWord(db.Model):
    __tablename__ = "user_words"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"))

    _user_word_idx = db.Index(
        "index_user_word", "user_id", "word_id", unique=True
    )
