from flask import Blueprint, render_template, abort, request

from app.services.building_service import get_building_dashboard

building_bp = Blueprint("building", __name__)


@building_bp.route("/properties/<int:property_id>/<int:building_id>")
def building_detail(property_id: int, building_id: int):
    tab = request.args.get("tab", "units")

    data = get_building_dashboard(property_id, building_id, tab)

    if not data:
        abort(404)

    return render_template(
        "building_detail.html", **data, page_title=data["building"].building_name
    )
