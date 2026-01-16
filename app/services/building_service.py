from app.repositories.property_repo import get_property_by_id
from app.repositories.building_repo import get_building_by_id_and_property

from app.utils.breadcrumbs import generate_breadcrumbs

def get_building_dashboard(property_id, building_id):
    property_obj = get_property_by_id(property_id)
    building_obj = get_building_by_id_and_property(building_id, property_id)

    breadcrumb = generate_breadcrumbs(property_id=property_id, building_id=building_id)

    if not property_obj or not building_obj:
        return None
    
    return {
        "building": building_obj,
        "units": building_obj.units,
        "breadcrumb": breadcrumb
    }