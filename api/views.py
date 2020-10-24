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

from db import queries
from db.models import User, UserWord, Word
from words_api.client import (
    WordsAPIClientError,
    WordsAPIServerError,
    words_api_client,
)

from .auth import generate_access_token, get_current_user
from .schema import (
    SignupSchema,
    UserInSchema,
    UserOutSchema,
    WordAPISchema,
    WordListSchema,
    WordSchema,
)

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
    words = await queries.get_user_words_with_variants(current_user.id)

    data = []
    for word in words:
        data.append(WordSchema.from_orm(word))

    return {"words": data}


@router.get("/search/{name}", response_model=WordSchema)
async def word_search(
    name: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    word = await queries.get_word_with_variants_by_name(name)
    if not word:
        try:
            data = await words_api_client.query_word(name)
        except (WordsAPIServerError, WordsAPIClientError):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Server error. Try later",
            )

        if not data:
            raise WordNotFound

        cleaned_data = WordAPISchema(**data).dict()

        word = await queries.add_new_word(**cleaned_data)

    return WordSchema.from_orm(word)


@router.post("/words/{word_id}", status_code=status.HTTP_201_CREATED)
async def word_add(
    word_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    word = await Word.get(word_id)
    if not word:
        raise WordNotFound

    try:
        await UserWord.create(user_id=current_user.id, word_id=word.id)
    except UniqueViolationError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Word already exists")


@router.delete("/words/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
async def word_remove(
    word_id: int, current_user: User = Depends(get_current_user)
):
    user_word = await UserWord.query.where(
        and_(UserWord.word_id == word_id, UserWord.user_id == current_user.id)
    ).gino.first()

    if not user_word:
        raise WordNotFound

    await user_word.delete()


def init_app(app: FastAPI):
    app.include_router(router)
