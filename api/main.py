import logging

from fastapi import FastAPI

from db import db
from words_api.client import words_api_client

from . import views

logger = logging.getLogger(__name__)

app = FastAPI(title="Vocabulary")

words_api_client.init_app(app)
db.init_app(app)
views.init_app(app)
