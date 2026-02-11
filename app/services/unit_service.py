from app.repositories.unit_repo import get_unit_by_id


def get_unit_dashboard(property_id, building_id, unit_id):
    unit_obj = get_unit_by_id(unit_id)

    return {"unit": unit_obj}
