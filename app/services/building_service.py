from app.repositories.property_repo import get_property_by_id
from app.repositories.building_repo import get_building_by_id_and_property
from app.repositories.unit_repo import (
    get_occupied_unit_ids,
    get_current_tennants_by_unit_ids,
    get_current_rent_by_unit_ids,
    get_outstanding_by_unit_ids
)

from app.utils.breadcrumbs import generate_breadcrumbs

def get_building_dashboard(property_id, building_id):
    property_obj = get_property_by_id(property_id)
    building_obj = get_building_by_id_and_property(building_id, property_id)

    if not property_obj or not building_obj:
        return None
    
    breadcrumb = generate_breadcrumbs(property_id=property_id, building_id=building_id)

    units = building_obj.units
    unit_ids = [unit.unit_id for unit in units]

    occupied_unit_ids = get_occupied_unit_ids(unit_ids)
    tenants_by_unit = get_current_tennants_by_unit_ids(unit_ids)
    rent_by_unit = get_current_rent_by_unit_ids(unit_ids)
    outstanding_by_unit = get_outstanding_by_unit_ids(unit_ids)


    units_data = []

    for unit in units:
        units_data.append({
            "unit": unit,
            "is_occupied": unit.unit_id in occupied_unit_ids,
            "tenants": tenants_by_unit.get(unit.unit_id, []),
            "current_rent": rent_by_unit.get(unit.unit_id),
            "outstanding_balance": outstanding_by_unit.get(unit.unit_id)
        })


    return {
        "building": building_obj,
        "units": units_data,
        "breadcrumb": breadcrumb
    }