from app.repositories.unit_repo import (
    get_unit_by_id, 
    get_occupied_unit_ids)
from app.utils.breadcrumbs import generate_breadcrumbs
from app.repositories.building_repo import get_building_by_id
from app.repositories.property_repo import get_property_by_id


def get_unit_dashboard(unit_id, tab):
    
    # Retrieve Tab Query from URL
    tenants = []
    leases = []
    documents = []
    
    if tab == "tenants":
        tenants = "tenants"
    
    # Retrieve Unit Object
    unit_obj = get_unit_by_id(unit_id)
    building_id = unit_obj.building_id
    
    # Retrieve Building Object
    building_obj = get_building_by_id(building_id)
    property_id = building_obj.property_id
    
    # Generate breadcrumb
    breadcrumb = generate_breadcrumbs(property_id, building_id, unit_id)
    
    # Check if the Unit has an active lease
    occupied = False
    occupied_set = get_occupied_unit_ids([unit_id])
    if len(occupied_set) > 0:
        occupied = True

        
    
    

    return {"unit": unit_obj,
            "tab": tab,
            "breadcrumb": breadcrumb,
            "occupied": occupied}
