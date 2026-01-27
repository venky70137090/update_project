import os


os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

from operations import app
from tables import init_db


init_db()