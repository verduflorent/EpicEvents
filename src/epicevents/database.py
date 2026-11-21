"""SQLAlchemy database connection utilities."""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from epicevents.config import database_url


def make_engine() -> Engine:
    """Create an SQLAlchemy engine from environment configuration."""
    return create_engine(database_url(), pool_pre_ping=True)


def check_connection(engine: Engine) -> bool:
    """Execute a minimal read-only query to validate database connectivity."""
    with engine.connect() as connection:
        return connection.execute(text("SELECT 1")).scalar_one() == 1
