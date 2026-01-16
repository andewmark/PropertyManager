from datetime import date

from sqlalchemy import distinct

from app.extensions import db
from app.models import Building, Unit, Lease

def get_occupied_unit_count(property_id):
    return (
        db.session.query(
            distinct(Unit.unit_id))
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