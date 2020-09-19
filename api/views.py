from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.get("/token")
async def login():
    pass


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
