from typing import List

from pydantic import BaseModel, EmailStr, Field, constr, validator


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


class WordVariantSchema(BaseModel):
    part_of_speech: str
    definition: str

    class Config:
        orm_mode = True


class WordSchema(BaseModel):
    id: int
    name: str
    variants: List[WordVariantSchema]

    class Config:
        orm_mode = True


class WordVariantAPISchema(BaseModel):
    part_of_speech: str = Field(alias="partOfSpeech")
    definition: str


class WordAPISchema(BaseModel):
    name: str = Field(alias="word")
    variants: List[WordVariantAPISchema] = Field(alias="results")


class WordListSchema(BaseModel):
    words: List[WordSchema] = []
