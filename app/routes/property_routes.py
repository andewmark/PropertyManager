from flask import Blueprint, render_template, abort
from app.services.property_service import (
    get_properties_overview,
    get_property_dashboard
)

property_bp = Blueprint("property", __name__)

@property_bp.route('/properties')
def properties():
    properties = get_properties_overview()

    return render_template(
        'properties.html',
        prop=properties,
        page_title="Properties"
    )

@property_bp.route('/properties/<int:property_id>')
def property_detail(property_id):
    data = get_property_dashboard(property_id)

    if not data:
        abort(404)

    return render_template(
        "property_details.html",
        **data,
        page_title=data["property"].property_name
    )