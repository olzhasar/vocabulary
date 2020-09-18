from fastapi import APIRouter, FastAPI

router = APIRouter()


@router.get("/")
async def index():
    return "Test"


def init_app(app: FastAPI):
    app.include_router(router)
