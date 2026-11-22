"""Entry point for the Epic Events command-line application."""

import click
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from epicevents.employees import EmployeeError, bootstrap_manager

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


@cli.command("bootstrap-manager")
@click.option("--name", prompt="Manager name")
@click.option("--email", prompt="Manager email")
@click.password_option(confirmation_prompt=True)
def bootstrap_manager_command(name: str, email: str, password: str) -> None:
    """Initialize the first management account on a trusted local installation."""
    try:
        engine = make_engine()
        try:
            with Session(engine) as session:
                with session.begin():
                    bootstrap_manager(session, name, email, password)
        finally:
            engine.dispose()
    except EmployeeError as error:
        raise click.ClickException(str(error)) from None
    except (RuntimeError, SQLAlchemyError, IntegrityError):
        raise click.ClickException(
            "Could not initialize account. Check database and account data."
        ) from None
    click.echo("Initial management account created.")


if __name__ == "__main__":
    cli()
