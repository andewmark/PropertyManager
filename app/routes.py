from flask import Blueprint, render_template
from sqlalchemy import func
from datetime import date
from app.models import Property, Unit, Building, Address
from app.extensions import db
from sqlalchemy import func, and_, distinct, text
from sqlalchemy.orm import aliased

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return render_template('dashboard.html', page_title="Dashboard")

@main.route("/health/db")
def db_health():
    db.session.execute(text("SELECT 1"))
    return {"status": "connected"}

@main.route('/properties')
def properties():
    # Create alias for main building (for address)
    MainBuilding = aliased(Building)
    MainAddress = aliased(Address)

    # Query
    results = (
        db.session.query(
            Property,
            func.count(distinct(Unit.unit_id)).label("unit_count"),       # all units across all buildings
            func.count(distinct(Building.building_id)).label("building_count"),  # all buildings
            func.concat(
                MainAddress.street_number, ' ',
                MainAddress.street, ', ',
                MainAddress.city, ', ',
                func.coalesce(MainAddress.state, ''), ' ',
                MainAddress.postal_code, ', ',
                MainAddress.country
            ).label("full_address")                                         # main building address
        )
        # join main building for full_address
        .outerjoin(MainBuilding, and_(
            MainBuilding.property_id == Property.property_id,
            MainBuilding.is_main_building == True
        ))
        .outerjoin(MainAddress, MainAddress.address_id == MainBuilding.address_id)

        # join all buildings and units to count them
        .outerjoin(Building, Building.property_id == Property.property_id)
        .outerjoin(Unit, Unit.building_id == Building.building_id)

        # group by property + main building address columns
        .group_by(
            Property.property_id,
            MainAddress.street_number,
            MainAddress.street,
            MainAddress.city,
            MainAddress.state,
            MainAddress.postal_code,
            MainAddress.country
        )
        .all()
    )

    return render_template(
        'properties.html',
        prop=results,
        page_title="Properties"
    )

# @main.route('/properties/<int:property_id>')
# def property_detail(property_id):
#     property_obj = Property.query.get(property_id)

#     today = date.today()
    
 
#     occupied_count = (
#         db.session.query(Unit)
#         .join(Lease)
#         .filter(
#             Unit.property_id == property_id,
#             Lease.start_date <= today,
#             Lease.end_date >= today,
#             Lease.cease_date == None  # optional
#         )
#         .count()
#     )

#     if not property_obj:
#         return "Property not found", 404
    
#     return render_template('property_details.html',
#                            prop=property_obj,
#                            page_title=property_obj.name,
#                            occupied_units=occupied_count)

@main.route('/payments')
def payments():
    return render_template('payments.html', page_title="Payments")

@main.route('/tenants')
def tenants():
    return render_template('tenants.html', page_title="Tenants")
