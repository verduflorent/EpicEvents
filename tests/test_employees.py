"""Tests for employee services using an isolated SQLite database."""

import pytest
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session

from epicevents.employees import (
    EmployeeError,
    bootstrap_manager,
    create_employee,
    delete_employee,
    hash_password,
    seed_departments,
    update_employee,
    verify_password,
)
from epicevents.models import Base, Department, Employee


@pytest.fixture
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enforce_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
        db.rollback()
    engine.dispose()


def test_password_is_salted_and_verifiable():
    first = hash_password("a-secure-passphrase")
    second = hash_password("a-secure-passphrase")
    assert first != second
    assert verify_password(first, "a-secure-passphrase")
    assert not verify_password(first, "incorrect-password")
    assert not verify_password("invalid", "a-secure-passphrase")


def test_password_too_short_is_rejected():
    with pytest.raises(EmployeeError):
        hash_password("short")


def test_bootstrap_is_one_time_only(session):
    manager = bootstrap_manager(
        session, "First Manager", "manager@example.com", "a-secure-passphrase"
    )
    assert manager.department.name == "gestion"
    assert len(session.scalars(select(Department)).all()) == 3
    with pytest.raises(EmployeeError, match="Bootstrap disabled"):
        bootstrap_manager(session, "Another", "other@example.com", "another-password")
    seed_departments(session)
    assert len(session.scalars(select(Department)).all()) == 3


def test_manager_can_create_update_and_delete(session):
    manager = bootstrap_manager(
        session, "Manager", "manager@example.com", "a-secure-passphrase"
    )
    employee = create_employee(
        session, manager, "Sales", "SALES@example.com", "another-password", "commercial"
    )
    assert employee.email == "sales@example.com"
    update_employee(session, manager, employee, department="support", name="Support")
    assert employee.department.name == "support"
    assert employee.full_name == "Support"
    delete_employee(session, manager, employee)
    assert session.get(Employee, employee.id) is None


def test_non_manager_cannot_manage_accounts(session):
    manager = bootstrap_manager(
        session, "Manager", "manager@example.com", "a-secure-passphrase"
    )
    sales = create_employee(
        session, manager, "Sales", "sales@example.com", "another-password", "commercial"
    )
    with pytest.raises(EmployeeError, match="Management permission"):
        create_employee(
            session, sales, "Other", "other@example.com", "another-password", "support"
        )
    with pytest.raises(EmployeeError, match="Management permission"):
        update_employee(session, sales, manager, name="New")
    with pytest.raises(EmployeeError, match="Management permission"):
        delete_employee(session, sales, manager)


def test_duplicate_email_and_self_deletion_rejected(session):
    manager = bootstrap_manager(
        session, "Manager", "manager@example.com", "a-secure-passphrase"
    )
    with pytest.raises(EmployeeError, match="Email already"):
        create_employee(
            session, manager, "Other", "MANAGER@example.com", "another-password", "support"
        )
    with pytest.raises(EmployeeError, match="own account"):
        delete_employee(session, manager, manager)
