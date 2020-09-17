import bcrypt
from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(100), nullable=False)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def check_password(self, password: str) -> bool:
        return self.password_hash == self.hash_password(password)

    def set_password(self, raw_password):
        self.password_hash = self.hash_password(raw_password)
