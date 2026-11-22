"""CLI tests without requiring a live PostgreSQL instance."""

from unittest.mock import patch

from click.testing import CliRunner

from epicevents.cli import cli


def test_cli_help():
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "db-check" in result.output


def test_db_check_success():
    with (
        patch("epicevents.cli.make_engine") as engine,
        patch("epicevents.cli.check_connection", return_value=True),
    ):
        result = CliRunner().invoke(cli, ["db-check"])
    assert result.exit_code == 0
    assert "Database connection OK." in result.output
    engine.return_value.dispose.assert_called_once()


def test_db_check_failure_hides_details():
    with patch("epicevents.cli.make_engine", side_effect=RuntimeError("secret")):
        result = CliRunner().invoke(cli, ["db-check"])
    assert result.exit_code != 0
    assert "secret" not in result.output
