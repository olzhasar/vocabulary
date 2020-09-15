from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException

from db import db, metadata
from db import sqlalchemy as sa

from .utils import hash_password

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("email", sa.String(255), nullable=False, index=True, unique=True),
    sa.Column("password_hash", sa.String(100), nullable=False),
)


class User:
    @classmethod
    async def get(cls, id=None, email=None):
        conditions = []
        if id:
            conditions.append(users.c.id == id)
        if email:
            conditions.append(users.c.email == email)
        if not conditions:
            raise HTTPException(400, "Either id or email must be provided")
        query = users.select().where(*conditions)
        user = await db.fetch_one(query)
        if not user:
            raise HTTPException(404, "User not found")
        return user

    @classmethod
    async def create(cls, **kwargs):
        kwargs["password_hash"] = hash_password(kwargs.pop("password"))
        query = users.insert().values(**kwargs)
        try:
            user_id = await db.execute(query)
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        return user_id
