"""Tests for the initial database connection layer."""

from unittest.mock import MagicMock, patch

import pytest

from epicevents.config import database_url
from epicevents.database import check_connection


def test_database_url_requires_configuration(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with patch("epicevents.config.load_dotenv"):
        with pytest.raises(RuntimeError, match="DATABASE_URL is missing"):
            database_url()


def test_check_connection_executes_select_one():
    engine = MagicMock()
    connection = engine.connect.return_value.__enter__.return_value
    connection.execute.return_value.scalar_one.return_value = 1

    assert check_connection(engine) is True
    assert connection.execute.call_args.args[0].text == "SELECT 1"
