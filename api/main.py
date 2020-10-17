import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from db import db
from words_api.client import words_api_client

from . import views

logger = logging.getLogger(__name__)

app = FastAPI(title="Vocabulary")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

words_api_client.init_app(app)
db.init_app(app)
views.init_app(app)
