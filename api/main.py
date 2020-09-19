import logging

from fastapi import FastAPI

from db import db

from . import views

logger = logging.getLogger(__name__)


app = FastAPI(title="Vocabulary")

db.init_app(app)
views.init_app(app)
