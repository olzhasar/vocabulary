from db import db, metadata
from db import sqlalchemy as sa

words = sa.Table(
    "words",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("word", sa.String(50), nullable=False, index=True, unique=True),
)
