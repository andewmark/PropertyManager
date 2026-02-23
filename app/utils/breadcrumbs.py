from app.repositories.property_repo import get_property_by_id
from app.repositories.building_repo import get_building_by_id
from app.repositories.unit_repo import get_unit_by_id


def generate_breadcrumbs(property_id=None, building_id=None, unit_id=None):
    breadcrumb = [{"name": "Properties", "url": "/properties"}]

    if property_id:
        property_obj = get_property_by_id(property_id)
        breadcrumb.append(
            {"name": property_obj.property_name, "url": f"/properties/{property_id}"}
        )

    if building_id:
        building_obj = get_building_by_id(property_id)
        breadcrumb.append(
            {
                "name": building_obj.building_name,
                "url": f"/properties/{property_id}/{building_id}",
            }
        )

    if unit_id:
        unit_obj = get_unit_by_id(unit_id)
        breadcrumb.append(
            {
                "name": unit_obj.unit_number,
                "url": f"/units/{unit_id}",
            }
        )

    return breadcrumb
