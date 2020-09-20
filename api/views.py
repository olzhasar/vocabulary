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

from db.models import User, UserWord, Word
from words_api.client import WordsAPIClient

from .auth import generate_access_token, get_current_user
from .schema import (
    SignupSchema,
    UserInSchema,
    UserOutSchema,
    WordListSchema,
    WordSchema,
)

router = APIRouter()


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


@router.get("/words/{word_id}", response_model=WordSchema)
async def word_get(
    word_id: int, current_user: User = Depends(get_current_user)
):
    word = await Word.get(word_id)
    return word


@router.post("/words/{word}", status_code=status.HTTP_201_CREATED)
async def word_add(
    word: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    word, _ = await Word.get_or_create(name=word)
    try:
        await UserWord.create(user_id=current_user.id, word_id=word.id)
    except UniqueViolationError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Word already exists")

    if not word.description:
        word.description = await WordsAPIClient.query_word(word)
        background_tasks.add_task(
            word.update(description=word.description).apply
        )

    return word.description


@router.delete("/words/{word}")
async def word_remove(
    word: str, current_user: User = Depends(get_current_user)
):
    return "Not implemented"


def init_app(app: FastAPI):
    app.include_router(router)
