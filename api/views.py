from typing import Any, Dict, Optional

from asyncpg.exceptions import UniqueViolationError
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_

from db.models import User, UserWord, Word
from words_api.client import (
    WordsAPIClientError,
    WordsAPIServerError,
    words_api_client,
)

from .auth import generate_access_token, get_current_user
from .schema import SignupSchema, UserInSchema, UserOutSchema, WordListSchema

router = APIRouter()


class WordNotFound(HTTPException):
    def __init__(
        self,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found",
            headers=headers,
        )


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid login credentials"
        )

    access_token = generate_access_token(email=user.email)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=UserOutSchema, status_code=201)
async def signup(data: SignupSchema):
    params = UserInSchema(**data.dict())

    existing = await User.get_by_email(params.email)
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already taken")

    user = await User.register(**params.dict())

    return user.__values__


@router.get("/words", response_model=WordListSchema)
async def word_list(current_user: User = Depends(get_current_user)):
    words = await (
        UserWord.load(word=Word)
        .query.where(UserWord.user_id == current_user.id)
        .gino.all()
    )

    words = [item.word.__values__ for item in words]

    return {"words": words}


@router.get("/search/{query}")
async def word_search(
    query: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    word = await Word.query.where(Word.name == query).gino.first()
    if word:
        return word.description

    try:
        description = await words_api_client.query_word(query)
    except (WordsAPIServerError, WordsAPIClientError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server error. Try later",
        )

    if not description:
        raise WordNotFound

    background_tasks.add_task(Word.create, name=query, description=description)

    return description


@router.post("/words/{query}", status_code=status.HTTP_201_CREATED)
async def word_add(
    query: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    word = await Word.query.where(Word.name == query).gino.first()
    if not word:
        raise WordNotFound
    word, _ = await Word.get_or_create(name=query)

    try:
        await UserWord.create(user_id=current_user.id, word_id=word.id)
    except UniqueViolationError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Word already exists")


@router.delete("/words/{word}", status_code=status.HTTP_204_NO_CONTENT)
async def word_remove(
    word_id: int, current_user: User = Depends(get_current_user)
):
    user_word = UserWord.query.where(
        and_(UserWord.word_id == word_id, UserWord.user_id == current_user.id)
    ).gino.first()

    if not user_word:
        raise WordNotFound

    await user_word.delete()


def init_app(app: FastAPI):
    app.include_router(router)
