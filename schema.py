from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr


class UserInSchema(UserSchema):
    password: str


class UserOutSchema(UserSchema):
    pass


class UserDBSchema(UserSchema):
    password_hash: str
