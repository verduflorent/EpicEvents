"""Employee account management, separate from the CLI and authentication."""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from epicevents.models import Department, Employee

DEPARTMENTS = ("gestion", "commercial", "support")
_hasher = PasswordHasher()


class EmployeeError(ValueError):
    """Invalid account operation or insufficient permissions."""


def hash_password(password: str) -> str:
    """Hash a password with Argon2id and a unique random salt."""
    if len(password) < 12:
        raise EmployeeError("Password must contain at least 12 characters.")
    return _hasher.hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a password without storing or logging its plaintext."""
    try:
        return _hasher.verify(stored_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def seed_departments(session: Session) -> None:
    """Insert the three departments once; safe to call repeatedly."""
    existing = set(session.scalars(select(Department.name)).all())
    for name in DEPARTMENTS:
        if name not in existing:
            session.add(Department(name=name))
    session.flush()


def _department(session: Session, name: str) -> Department:
    department = session.scalar(select(Department).where(Department.name == name))
    if department is None:
        raise EmployeeError("Unknown department.")
    return department


def _manager(actor: Employee | None) -> None:
    if actor is None or actor.department.name != "gestion":
        raise EmployeeError("Management permission required.")


def _validated_identity(name: str, email: str) -> tuple[str, str]:
    name = name.strip()
    email = email.strip().lower()
    if not name or len(name) > 150:
        raise EmployeeError("Invalid employee name.")
    if not email or len(email) > 254 or email.count("@") != 1:
        raise EmployeeError("Invalid employee email.")
    return name, email


def _create(
    session: Session, name: str, email: str, password: str, department: str
) -> Employee:
    name, email = _validated_identity(name, email)
    if session.scalar(select(Employee.id).where(Employee.email == email)) is not None:
        raise EmployeeError("Email already registered.")
    employee = Employee(
        full_name=name,
        email=email,
        password_hash=hash_password(password),
        department=_department(session, department),
    )
    session.add(employee)
    session.flush()
    return employee


def bootstrap_manager(
    session: Session, name: str, email: str, password: str
) -> Employee:
    """Create the first manager only when no employee exists.

    Call only from a trusted local setup command, not from a public endpoint.
    """
    if session.scalar(select(func.count(Employee.id))) != 0:
        raise EmployeeError("Bootstrap disabled: employees already exist.")
    seed_departments(session)
    return _create(session, name, email, password, "gestion")


def create_employee(
    session: Session,
    actor: Employee,
    name: str,
    email: str,
    password: str,
    department: str,
) -> Employee:
    """Create an employee only when the actor belongs to management."""
    _manager(actor)
    return _create(session, name, email, password, department)


def update_employee(
    session: Session,
    actor: Employee,
    employee: Employee,
    *,
    name: str | None = None,
    email: str | None = None,
    department: str | None = None,
) -> Employee:
    """Change employee identity and department, with management authorization."""
    _manager(actor)
    if name is not None or email is not None:
        updated_name, updated_email = _validated_identity(
            name if name is not None else employee.full_name,
            email if email is not None else employee.email,
        )
        existing = session.scalar(
            select(Employee).where(Employee.email == updated_email)
        )
        if existing is not None and existing.id != employee.id:
            raise EmployeeError("Email already registered.")
        employee.full_name = updated_name
        employee.email = updated_email
    if department is not None:
        employee.department = _department(session, department)
    session.flush()
    return employee


def delete_employee(session: Session, actor: Employee, employee: Employee) -> None:
    """Delete an unreferenced employee; never allow self-deletion."""
    _manager(actor)
    if actor.id == employee.id:
        raise EmployeeError("Managers cannot delete their own account.")
    session.delete(employee)
    session.flush()
    # Existing client/contract references are protected by database FK rules.
