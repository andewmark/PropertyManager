from app.repositories.property_repo import (
    fetch_properties_with_summary,
    get_property_by_id
)

from app.repositories.unit_repo import (
    get_occupied_unit_count,
    get_total_unit_count
)

from app.repositories.finance_repo import (
    get_rent_collected,
    get_rent_due,
    get_next_rent_due_date,
    get_total_outstanding
)

from app.utils.dates import current_month_bounds
from app.utils.breadcrumbs import generate_breadcrumbs

def get_properties_overview():
    """
    High-level intent:
        'Give me all properties with counts and primary address'
    """
    return fetch_properties_with_summary()

def get_property_dashboard(property_id):
    property_obj = get_property_by_id(property_id)

    if not property_obj:
        return None
    
    today, first_day, next_month = current_month_bounds()

    unit_occupied_count = get_occupied_unit_count(property_id)
    total_unit_count = get_total_unit_count(property_id)
    
    occupancy_rate = (int)((unit_occupied_count / total_unit_count)*100)

    rent_collected = get_rent_collected(first_day, next_month)
    rent_due = get_rent_due(first_day, next_month)
    next_rent_due = get_next_rent_due_date(first_day,next_month)
    total_outstanding = get_total_outstanding(today)

    breadcrumb = generate_breadcrumbs(property_id)
    
    return {
        "property": property_obj,
        "buildings": property_obj.buildings,
        "total_units":  total_unit_count,
        "unit_occupied_count": unit_occupied_count,
        "occupancy_rate": occupancy_rate,
        "rent_collected": rent_collected,
        "rent_due": rent_due,
        "next_rent_due": next_rent_due,
        "total_outstanding": total_outstanding,
        "is_under_collected": rent_collected < rent_due,
        "breadcrumb": breadcrumb
    }