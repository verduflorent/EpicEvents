"""Entry point for the Epic Events command-line application."""

import click
from sqlalchemy.exc import SQLAlchemyError

from epicevents.database import check_connection, make_engine


@click.group()
def cli() -> None:
    """Epic Events CRM."""


@cli.command("db-check")
def db_check() -> None:
    """Verify access to the configured PostgreSQL database."""
    try:
        engine = make_engine()
        try:
            if check_connection(engine):
                click.echo("Database connection OK.")
            else:
                raise click.ClickException("Database check failed.")
        finally:
            engine.dispose()
    except (RuntimeError, SQLAlchemyError):
        # Do not print driver exceptions: they may contain connection details.
        raise click.ClickException(
            "Database unavailable. Check DATABASE_URL and PostgreSQL."
        ) from None


if __name__ == "__main__":
    cli()
