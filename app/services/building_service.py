from app.repositories.property_repo import get_property_by_id
from app.repositories.building_repo import get_building_by_id_and_property
from app.utils.dates import current_month_bounds
from app.repositories.unit_repo import (
    get_occupied_unit_ids,
    get_current_tennants_by_unit_ids,
    get_current_rent_by_unit_ids,
    get_outstanding_by_unit_ids,
)
from app.repositories.finance_repo import (
    get_rent_collected_by_building,
    get_rent_due_by_building,
    get_building_next_rent_due_date,
    get_total_outstanding_for_building,
)

from app.utils.breadcrumbs import generate_breadcrumbs


def get_building_dashboard(property_id, building_id):
    property_obj = get_property_by_id(property_id)
    building_obj = get_building_by_id_and_property(building_id, property_id)

    today, first_day, next_month = current_month_bounds()

    if not property_obj or not building_obj:
        return None

    breadcrumb = generate_breadcrumbs(property_id=property_id, building_id=building_id)

    units = building_obj.units
    unit_ids = [unit.unit_id for unit in units]

    # Retrieve per Unit data
    occupied_unit_ids = get_occupied_unit_ids(unit_ids)
    tenants_by_unit = get_current_tennants_by_unit_ids(unit_ids)
    rent_by_unit = get_current_rent_by_unit_ids(unit_ids)
    outstanding_by_unit = get_outstanding_by_unit_ids(unit_ids)

    units_data = []

    for unit in units:
        units_data.append(
            {
                "unit": unit,
                "is_occupied": unit.unit_id in occupied_unit_ids,
                "tenants": tenants_by_unit.get(unit.unit_id, []),
                "current_rent": rent_by_unit.get(unit.unit_id),
                "outstanding_balance": outstanding_by_unit.get(unit.unit_id),
            }
        )

    # Retrieve Building data
    unit_occupied_count = len(occupied_unit_ids)
    total_units = len(unit_ids)
    occupancy_rate = (int)((unit_occupied_count / total_units) * 100)

    rent_collected = get_rent_collected_by_building(first_day, next_month, building_id)
    rent_due = get_rent_due_by_building(first_day, next_month, building_id)
    next_rent_due = get_building_next_rent_due_date(first_day, next_month, building_id)
    total_outstanding = get_total_outstanding_for_building(today, building_id)

    return {
        "building": building_obj,
        "units": units_data,
        "unit_occupied_count": unit_occupied_count,
        "total_units": total_units,
        "occupancy_rate": occupancy_rate,
        "rent_collected": rent_collected,
        "rent_due": rent_due,
        "is_under_collected": rent_collected < rent_due,
        "total_outstanding": total_outstanding,
        "next_rent_due": next_rent_due,
        "breadcrumb": breadcrumb,
    }
