from flask import Blueprint, render_template
from app.services.unit_service import get_unit_dashboard

unit_bp = Blueprint("unit", __name__)


@unit_bp.route("/properties/<int:property_id>/<int:building_id>/<int:unit_id>")
def unit_detail(property_id, building_id, unit_id):
    data = get_unit_dashboard(property_id, building_id, unit_id)

    return render_template(
        "unit_details.html", **data, page_title=data["unit"].unit_number
    )
