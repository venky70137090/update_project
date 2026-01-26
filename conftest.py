import os

# Set a test database URL for pytest runs to avoid hitting production CockroachDB
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")

# Now import the app and tables after setting the env var
from operations import app
from tables import init_db

# Initialize the test database schema
init_db()