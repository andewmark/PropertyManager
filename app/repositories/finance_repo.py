from sqlalchemy import func

from app.extensions import db
from app.models import Application, Charges


def get_rent_collected(first_day, next_month):
    return (
        db.session.query(
            func.coalesce(func.sum(Application.amount_applied), 0)
        ).join(Charges, Application.charge_id == Charges.charge_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day
        )
        .scalar()
    )

def get_rent_due(first_day, next_month):
    return (
        db.session.query(
            func.coalesce(func.sum(Charges.amount), 0)
        ).filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day
        )
        .scalar()
    )

def get_next_rent_due_date(first_day, next_month):
    return (
            db.session.query(
                Charges.due_date
            ).filter(
                Charges.charge_type == "rent",
                Charges.period_start < next_month,
                Charges.period_end >= first_day
            )
            .order_by(Charges.due_date.asc())
            .limit(1)
            .scalar()
        )

def get_total_outstanding(today):
    applied_subq = (
        db.session.query(
            Application.charge_id.label("charge_id"),
            func.sum(Application.amount_applied).label("total_applied")
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
                0
            )
        )
        .outerjoin(
            applied_subq,
            applied_subq.c.charge_id == Charges.charge_id
        )
        .filter(
            Charges.status.notin_(["paid", "void"]),
            Charges.due_date <= today
        )
        .scalar()
    )