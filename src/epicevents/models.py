"""Relational models for Epic Events.

This module defines the database structure only. Business permissions and
password hashing are implemented in later milestones.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Shared SQLAlchemy declarative base."""


class Department(Base):
    """An Epic Events team (management, sales, or support)."""

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    employees: Mapped[list["Employee"]] = relationship(back_populates="department")


class Employee(Base):
    """A collaborator assigned to a department."""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False
    )

    department: Mapped[Department] = relationship(back_populates="employees")
    clients: Mapped[list["Client"]] = relationship(
        back_populates="sales_contact", foreign_keys="Client.sales_contact_id"
    )
    contracts: Mapped[list["Contract"]] = relationship(
        back_populates="sales_contact", foreign_keys="Contract.sales_contact_id"
    )
    assigned_events: Mapped[list["Event"]] = relationship(
        back_populates="support_contact", foreign_keys="Event.support_contact_id"
    )


class Client(Base):
    """Customer whose commercial contact is an Epic Events employee."""

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    company_name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    sales_contact_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False
    )

    sales_contact: Mapped[Employee] = relationship(
        back_populates="clients", foreign_keys=[sales_contact_id]
    )
    contracts: Mapped[list["Contract"]] = relationship(back_populates="client")


class Contract(Base):
    """Commercial agreement associated with one client."""

    __tablename__ = "contracts"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_contract_total_nonnegative"),
        CheckConstraint(
            "remaining_amount >= 0", name="ck_contract_remaining_nonnegative"
        ),
        CheckConstraint(
            "remaining_amount <= total_amount", name="ck_contract_remaining_lte_total"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="RESTRICT"), nullable=False
    )
    sales_contact_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    remaining_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_signed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    client: Mapped[Client] = relationship(back_populates="contracts")
    sales_contact: Mapped[Employee] = relationship(
        back_populates="contracts", foreign_keys=[sales_contact_id]
    )
    events: Mapped[list["Event"]] = relationship(back_populates="contract")


class Event(Base):
    """Event linked to a contract and optionally assigned to support."""

    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("attendees >= 0", name="ck_event_attendees_nonnegative"),
        CheckConstraint("ends_at > starts_at", name="ck_event_end_after_start"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id", ondelete="RESTRICT"), nullable=False
    )
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(String(300), nullable=False)
    attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    support_contact_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )

    contract: Mapped[Contract] = relationship(back_populates="events")
    support_contact: Mapped[Employee | None] = relationship(
        back_populates="assigned_events", foreign_keys=[support_contact_id]
    )
