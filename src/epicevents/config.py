"""Application configuration from local environment variables."""

import os

from dotenv import load_dotenv


def database_url() -> str:
    """Return the configured database URL without embedding credentials in code."""
    load_dotenv()
    value = os.getenv("DATABASE_URL")
    if not value:
        raise RuntimeError("DATABASE_URL is missing. Configure your local .env file.")
    return value
