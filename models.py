from db import db, metadata, sqlalchemy
from db.sqlalchemy import Column, Integer, String

users = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(255), nullable=False, index=True, unique=True),
    Column("password_hash", String(100), nullable=False),
)


class User:
    @classmethod
    async def get(cls, id):
        query = users.select().where(users.c.id == id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def create(cls, **kwargs):
        query = users.insert().values(**kwargs)
        user_id = await db.execute(query)
        return user_id
