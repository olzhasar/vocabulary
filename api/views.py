from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.models import User

from .schema import SignupSchema, UserInSchema, UserOutSchema
from .utils import generate_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

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

    access_token = generate_access_token({"email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=UserOutSchema, status_code=201)
async def signup(data: SignupSchema):
    params = UserInSchema(**data.dict())

    existing = await User.get_by_email(params.email)
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already taken")

    user = await User.register(**params.dict())
    return user.__values__


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
