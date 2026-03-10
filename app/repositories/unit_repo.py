from datetime import date

from sqlalchemy import distinct, func

from app.extensions import db
from app.models import (
    Building,
    Unit,
    Lease,
    Tenants,
    Application,
    Charges,
    Payments,
    PropertyExpenses,
)


def get_occupied_unit_count(property_id):
    return (
        db.session.query(distinct(Unit.unit_id))
        .join(Lease)
        .join(Building)
        .filter(Building.property_id == property_id)
        .filter(Lease.start_date <= date.today())
        .filter(Lease.end_date >= date.today())
        .filter(Lease.move_out_date.is_(None))
        .count()
    )


def get_total_unit_count(property_id):
    return (
        db.session.query(Unit.unit_id)
        .join(Building)
        .filter(Building.property_id == property_id)
        .count()
    )


def get_unit_by_id(unit_id):
    return Unit.query.get(unit_id)


def get_occupied_unit_ids(unit_ids):
    """
    Get Occupied units by unit_id based on if they have an acitve lease

    Args:
        unit_ids (Arr[Ints]): List of unit_ids

    Returns:
        set[int]: occupied unit ids
    """
    return {
        row.unit_id
        for row in (
            db.session.query(Lease.unit_id)
            .filter(Lease.unit_id.in_(unit_ids))
            .filter(Lease.start_date <= date.today())
            .filter(Lease.end_date >= date.today())
            .filter(Lease.move_out_date.is_(None))
            .distinct()
            .all()
        )
    }


def get_current_tennants_by_unit_ids(unit_ids):
    """
    Get current tenants given a list of unit ids

    Args:
        unit_ids (Arr[Ints]): List of unit_ids

    Returns:
        dict - {unit_id: [tenants]}: mapping of units to active tenants
    """
    rows = (
        db.session.query(Lease.unit_id, Tenants)
        .join(Tenants, Tenants.tenant_id == Lease.tenant_id)
        .filter(Lease.unit_id.in_(unit_ids))
        .filter(Lease.start_date <= date.today())
        .filter(Lease.end_date >= date.today())
        .filter(Lease.move_out_date.is_(None))
        .all()
    )

    tenants_by_unit = {}

    for unit_id, tenant in rows:
        tenants_by_unit.setdefault(unit_id, []).append(tenant)

    return tenants_by_unit


def get_current_rent_by_unit_ids(unit_ids):
    today = date.today()

    active_lease_rent_subq = (
        db.session.query(
            Lease.unit_id.label("unit_id"), func.sum(Lease.rent).label("active_rent")
        )
        .filter(Lease.start_date <= today)
        .filter(Lease.end_date >= today)
        .filter(Lease.move_out_date.is_(None))
        .group_by(Lease.unit_id)
        .subquery()
    )

    rows = (
        db.session.query(
            Unit.unit_id,
            func.coalesce(active_lease_rent_subq.c.active_rent, Unit.market_rent).label(
                "rent_amount"
            ),
        )
        .outerjoin(
            active_lease_rent_subq, active_lease_rent_subq.c.unit_id == Unit.unit_id
        )
        .filter(Unit.unit_id.in_(unit_ids))
        .all()
    )

    return {row.unit_id: row.rent_amount for row in rows}


def get_outstanding_by_unit_ids(unit_ids):
    today = date.today()

    applied_subq = (
        db.session.query(
            Application.charge_id.label("charge_id"),
            func.sum(Application.amount_applied).label("total_applied"),
        )
        .group_by(Application.charge_id)
        .subquery()
    )

    rows = (
        db.session.query(
            Lease.unit_id.label("unit_id"),
            func.coalesce(
                func.sum(
                    Charges.amount - func.coalesce(applied_subq.c.total_applied, 0)
                ),
                0,
            ).label("outstanding_amount"),
        )
        .join(Lease, Lease.lease_id == Charges.lease_id)
        .outerjoin(applied_subq, applied_subq.c.charge_id == Charges.charge_id)
        .filter(
            Charges.status.notin_(["paid", "void"]),
            Charges.due_date <= today,
            Lease.unit_id.in_(unit_ids),
        )
        .group_by(Lease.unit_id)
        .all()
    )

    return {row.unit_id: row.outstanding_amount for row in rows}


def get_current_lease_by_unit_id(unit_id):
    today = date.today()

    return (
        db.session.query(Lease.lease_id)
        .filter(Lease.unit_id == unit_id)
        .filter(Lease.start_date <= today)
        .filter(Lease.end_date > today)
        .filter(Lease.move_out_date.is_(None))
        .all()
    )


def get_unit_YTD_payments(unit_id):
    year = date(date.today().year, 1, 1)

    return (
        db.session.query(func.sum(Payments.payment_amount))
        .join(Lease, Lease.lease_id == Payments.lease_id)
        .join(Unit, Unit.unit_id == Lease.unit_id)
        .filter(Unit.unit_id == unit_id)
        .filter(
            Payments.payment_status == "Completed"
        )  # TODO: Don't include String Literals
        .filter(Payments.payment_date >= year)
        .scalar()
    )


def get_unit_YTD_expenses(unit_id):
    year = date(date.today().year, 1, 1)

    return (
        db.session.query(func.sum(PropertyExpenses.expense_amount))
        .filter(Unit.unit_id == unit_id)
        .filter(PropertyExpenses.date_incurred >= year)
        .scalar()
    )
