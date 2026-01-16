from sqlalchemy.orm import aliased
from sqlalchemy import func, distinct, and_ 

from app.extensions import db
from app.models import Property, Building, Unit, Address

def fetch_properties_with_summary():
    """
    Returns:
        List of rows containing:
        - Property
        - unit_count
        - building_count
        - full_address (of the main building)
    """
    MainBuilding = aliased(Building)
    MainAddress = aliased(Address)

    return (
        db.session.query(
            Property,
            func.count(distinct(Unit.unit_id)).label("unit_count"),       # all units across all buildings
            func.count(distinct(Building.building_id)).label("building_count"),  # all buildings
            func.concat(
                MainAddress.street_number, ' ',
                MainAddress.street, ', ',
                MainAddress.city, ', ',
                func.coalesce(MainAddress.state, ''), ' ',
                MainAddress.postal_code, ', ',
                MainAddress.country
            ).label("full_address")                                         # main building address
        )
        # join main building for full_address
        .outerjoin(MainBuilding, and_(
            MainBuilding.property_id == Property.property_id,
            MainBuilding.is_main_building == True
        ))
        .outerjoin(MainAddress, MainAddress.address_id == MainBuilding.address_id)

        # join all buildings and units to count them
        .outerjoin(Building, Building.property_id == Property.property_id)
        .outerjoin(Unit, Unit.building_id == Building.building_id)

        # group by property + main building address columns
        .group_by(
            Property.property_id,
            MainAddress.street_number,
            MainAddress.street,
            MainAddress.city,
            MainAddress.state,
            MainAddress.postal_code,
            MainAddress.country
        )
        .all()
    )

def get_property_by_id(property_id):
    return Property.query.get(property_id)