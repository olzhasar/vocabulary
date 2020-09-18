from pydantic import BaseModel, EmailStr, constr, validator


class UserSchema(BaseModel):
    email: EmailStr


class UserInSchema(UserSchema):
    password: str


class UserOutSchema(UserSchema):
    pass


class SignupSchema(UserInSchema):
    password: constr(min_length=8)
    repeat_password: str

    @validator("repeat_password")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v
