from typing import Optional
from app.models import Building


def get_building_by_id(building_id: int) -> Optional[Building]:
    return Building.query.get(building_id)


def get_building_by_id_and_property(
    building_id: int, property_id: int
) -> Optional[Building]:
    return Building.query.filter_by(
        building_id=building_id, property_id=property_id
    ).first()
