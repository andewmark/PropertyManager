from typing import Optional
from app.extensions import db
from sqlalchemy import distinct
from app.models import Building, Maintenance


def get_building_by_id(building_id: int) -> Optional[Building]:
    return Building.query.get(building_id)


def get_building_by_id_and_property(
    building_id: int, property_id: int
) -> Optional[Building]:
    return Building.query.filter_by(
        building_id=building_id, property_id=property_id
    ).first()


def get_active_building_maintenance(building_id: int) -> int:
    return (
        db.session.query(distinct(Maintenance.maintenance_id))
        .filter(Maintenance.building_id == building_id)
        .filter(Maintenance.date_completed.is_(None))
        .count()
    )
