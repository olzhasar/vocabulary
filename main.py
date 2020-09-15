import uvicorn
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import app
from users.models import User
from users.schema import UserInSchema, UserOutSchema
from words_api import WordsAPIClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.on_event("startup")
def startup_event():
    WordsAPIClient.get_session()


@app.on_event("shutdown")
async def shutdown_event():
    await WordsAPIClient.close_session


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = User.get(email=form_data.username)
    if not user_record:
        raise HTTPException(400, "Wrong username or password")
    user = UserOutSchema(user_record)
    return {"access_token": user.email, "token_type": "bearer"}


@app.post("/signup/")
async def signup(user: UserInSchema):
    user_id = await User.create(**user.dict())
    return {"user_id": user_id}


@app.get("/words/{word}")
async def fetch_word(word: str, token: str = Depends(oauth2_scheme)):
    result = await WordsAPIClient.query_word(word)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
