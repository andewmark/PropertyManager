from sqlalchemy import func
from datetime import date
from decimal import Decimal

from app.extensions import db
from app.models import Application, Charges, Lease, Unit, Building


def get_rent_collected_by_property(first_day: date, next_month: date, property_id: int) -> Decimal | None:
    """
    Gets all charges and applicable payment applications to retrieve sum
    of rent collected for the specified property within the given period.

    :param first_day: First day of the month
    :param next_month: First day of the next month
    :param property_id: property_id
    """
    return (
        db.session.query(func.coalesce(func.sum(Application.amount_applied), 0))
        .join(Charges, Application.charge_id == Charges.charge_id)
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .join(Building, Unit.building_id == Unit.building_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day,
            Building.property_id == property_id,
        )
        .scalar()
    )


def get_rent_collected_by_building(first_day: date, next_month: date, building_id: int) -> Decimal | None:
    """
    Gets all charges and applicable payment applications to retrieve sum
    of rent collected for the specified building within the given period.

    :param first_day: First day of the month
    :param next_month: First day of the next month
    :param building_id: building_id
    """
    return (
        db.session.query(func.coalesce(func.sum(Application.amount_applied), 0))
        .join(Charges, Application.charge_id == Charges.charge_id)
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day,
            Unit.building_id == building_id,
        )
        .scalar()
    )


def get_rent_due_by_property(first_day: date, next_month: date, property_id: int) -> Decimal | None:
    """
    Gets all rent due for specified property within the given period

    :param first_day: First day of the month
    :param next_month: First day of the next month
    :param property_id: property_id
    """
    return (
        db.session.query(func.coalesce(func.sum(Charges.amount), 0))
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .join(Building, Unit.building_id == Unit.building_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day,
            Building.property_id == property_id,
        )
        .scalar()
    )


def get_rent_due_by_building(first_day: date, next_month: date, building_id: int) -> Decimal | None:
    """
    Gets all rent due for specified property within the given period

    :param first_day: First day of the month
    :param next_month: First day of the next month
    :param building_id: building_id
    """
    return (
        db.session.query(func.coalesce(func.sum(Charges.amount), 0))
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day,
            Unit.building_id == building_id,
        )
        .scalar()
    )


def get_property_next_rent_due_date(first_day: date, next_month: date, property_id: int) -> Decimal | None:
    return (
        db.session.query(Charges.due_date)
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .join(Building, Unit.building_id == Unit.building_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day,
            Building.property_id == property_id,
        )
        .order_by(Charges.due_date.asc())
        .limit(1)
        .scalar()
    )


def get_building_next_rent_due_date(first_day: date, next_month: date, building_id: int) -> Decimal | None:
    return (
        db.session.query(Charges.due_date)
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day,
            Unit.building_id == building_id,
        )
        .order_by(Charges.due_date.asc())
        .limit(1)
        .scalar()
    )


def get_total_outstanding_for_property(today: date, property_id: int) -> Decimal | None:
    """
    Gets outstanding balance for the given property passed in

    :param today: Today
    :param property_id: Property 
    """
    applied_subq = (
        db.session.query(
            Application.charge_id.label("charge_id"),
            func.sum(Application.amount_applied).label("total_applied"),
        )
        .group_by(Application.charge_id)
        .subquery()
    )

    return (
        db.session.query(
            func.coalesce(
                func.sum(
                    Charges.amount - func.coalesce(applied_subq.c.total_applied, 0)
                ),
                0,
            )
        )
        .outerjoin(applied_subq, applied_subq.c.charge_id == Charges.charge_id)
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .join(Building, Unit.building_id == Unit.building_id)
        .filter(
            Charges.status.notin_(["paid", "void"]),
            Charges.due_date <= today,
            Building.property_id == property_id,
        )
        .scalar()
    )


def get_total_outstanding_for_building(today: date, building_id: int) -> Decimal | None:
    applied_subq = (
        db.session.query(
            Application.charge_id.label("charge_id"),
            func.sum(Application.amount_applied).label("total_applied"),
        )
        .group_by(Application.charge_id)
        .subquery()
    )

    return (
        db.session.query(
            func.coalesce(
                func.sum(
                    Charges.amount - func.coalesce(applied_subq.c.total_applied, 0)
                ),
                0,
            )
        )
        .outerjoin(applied_subq, applied_subq.c.charge_id == Charges.charge_id)
        .join(Lease, Charges.lease_id == Lease.lease_id)
        .join(Unit, Lease.unit_id == Unit.unit_id)
        .filter(
            Charges.status.notin_(["paid", "void"]),
            Charges.due_date <= today,
            Unit.building_id == building_id,
        )
        .scalar()
    )
