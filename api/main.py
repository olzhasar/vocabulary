import logging

from fastapi import FastAPI

from db import db

logger = logging.getLogger(__name__)


def get_app():
    app = FastAPI(title="Vocabulary")
    db.init_app(app)
    return app
