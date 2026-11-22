"""Validate the schema and its relationships without a live database."""

from sqlalchemy import CheckConstraint, ForeignKey

from epicevents.models import Base, Client, Contract, Department, Employee, Event


def test_expected_tables_are_registered():
    assert set(Base.metadata.tables) == {
        "departments",
        "employees",
        "clients",
        "contracts",
        "events",
    }


def test_relationships_have_foreign_keys():
    expected = {
        "employees": {"departments.id"},
        "clients": {"employees.id"},
        "contracts": {"clients.id", "employees.id"},
        "events": {"contracts.id", "employees.id"},
    }
    for table_name, targets in expected.items():
        table = Base.metadata.tables[table_name]
        actual = {
            fk.target_fullname
            for column in table.columns
            for fk in column.foreign_keys
        }
        assert actual == targets


def test_constraints_protect_contract_amounts_and_event_dates():
    for table_name, expected in (
        ("contracts", {"ck_contract_total_nonnegative", "ck_contract_remaining_nonnegative", "ck_contract_remaining_lte_total"}),
        ("events", {"ck_event_attendees_nonnegative", "ck_event_end_after_start"}),
    ):
        constraints = {
            item.name
            for item in Base.metadata.tables[table_name].constraints
            if isinstance(item, CheckConstraint)
        }
        assert constraints == expected


def test_support_assignment_is_optional():
    assert Event.__table__.c.support_contact_id.nullable
    assert not Client.__table__.c.sales_contact_id.nullable
    assert not Employee.__table__.c.department_id.nullable


def test_model_relationship_attributes_exist():
    assert Department.employees
    assert Employee.clients
    assert Client.contracts
    assert Contract.events
    assert Event.support_contact
