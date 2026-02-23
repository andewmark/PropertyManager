from flask import Blueprint, render_template, request
from app.services.unit_service import get_unit_dashboard

unit_bp = Blueprint("unit", __name__)


@unit_bp.route("/units/<int:unit_id>")
def unit_detail( unit_id):
    tab = request.args.get("tab", "tenants")
    
    data = get_unit_dashboard(unit_id, tab)

    return render_template(
        "unit_details.html", **data, page_title=f"Unit {data["unit"].unit_number}"
    )
