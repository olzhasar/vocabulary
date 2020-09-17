import logging
from importlib.metadata import entry_points

import click
from fastapi import FastAPI

from config.db import db

logger = logging.getLogger(__name__)


def get_app():
    app = FastAPI(title="GINO FastAPI Demo")
    db.init_app(app)
    # load_modules(app)
    return app


def load_modules(app=None):
    for ep in entry_points():
        logger.info(
            "Loading module: %s",
            ep.name,
            extra={
                "color_message": "Loading module: "
                + click.style("%s", fg="cyan")
            },
        )
        mod = ep.load()
        if app:
            init_app = getattr(mod, "init_app", None)
            if init_app:
                init_app(app)
