import os

import sqlalchemy
from databases import Database

from settings import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if settings.TESTING:
    db = Database(settings.TEST_DATABASE_URL, force_rollback=True)
else:
    db = Database(settings.DATABASE_URL)

metadata = sqlalchemy.MetaData()
