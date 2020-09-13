import uvicorn

from app import app
from models import User
from schema import UserInSchema, UserOutSchema
from words_api import WordsAPIClient


@app.on_event("startup")
def startup_event():
    WordsAPIClient.get_session()


@app.on_event("shutdown")
async def shutdown_event():
    await WordsAPIClient.close_session


@app.post("/user/")
async def create_user(user: UserInSchema):
    user_id = await User.create(**user.dict())
    return {"user_id": user_id}


@app.get("/user/{id}", response_model=UserOutSchema)
async def get_user(id: int):
    user = await User.get(id)
    return UserOutSchema(**user).dict()


@app.get("/words/{word}")
async def fetch_word(word: str):
    result = await WordsAPIClient.query_word(word)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
