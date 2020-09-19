from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.models import User

from .utils import generate_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter()


@router.get("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(**form_data)
    if not user:
        raise HTTPException(401, "Invalid login credentials")

    access_token = generate_access_token({"email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/signup")
async def signup():
    pass


@router.get("/words")
async def word_list():
    return "Not implemented"


@router.get("/words/{word}")
async def word_get(word: str):
    return "Not implemented"


@router.post("/words")
async def word_add():
    return "Not implemented"


@router.delete("/words/{word}")
async def word_remove(word: str):
    return "Not implemented"


def init_app(app: FastAPI):
    app.include_router(router)
