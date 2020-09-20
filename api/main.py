import logging

from fastapi import FastAPI

from db import db
from words_api.client import WordsAPIClient

from . import views

logger = logging.getLogger(__name__)


app = FastAPI(title="Vocabulary")


@app.on_event("startup")
def startup_event():
    WordsAPIClient.get_session()


@app.on_event("shutdown")
async def shutdown_event():
    await WordsAPIClient.close_session()


db.init_app(app)
views.init_app(app)
