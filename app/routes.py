from flask import Blueprint, render_template, abort
from sqlalchemy import func
from datetime import date
from app.models import Property, Unit, Building, Address, BuildingType, Lease, Payments, Charges, Application
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



@main.route('/properties/<int:property_id>')
def property_detail(property_id):
    property_obj = Property.query.get(property_id)
    buildings_obj = property_obj.buildings

    # Unit Occupancy
    unit_occupied_count = (
        db.session.query(
            distinct(Unit.unit_id))
            .join(Lease)
            .join(Building)
            .filter(Building.property_id == property_id)
            .filter(Lease.start_date <= date.today())
            .filter(Lease.end_date >= date.today())
            .filter(Lease.move_out_date.is_(None))
            .count()
        )
    
    # Total Units
    total_units = (
        db.session.query(
            Unit.unit_id)
        .join(Building)
        .filter(Building.property_id == property_id)
        .count()
    )

    # Rent Collected This Month
    today = date.today()
    first_day = today.replace(day=1)
    if today.month == 12:
        next_month = today.replace(year=today.year+1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month+1, day=1)
    
    rent_collected = (
        db.session.query(
            func.coalesce(func.sum(Application.amount_applied), 0)
        ).join(Charges, Application.charge_id == Charges.charge_id)
        .filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day
        )
        .scalar()
    )

    # Rent Owed This Month
    rent_due = (
        db.session.query(
            func.coalesce(func.sum(Charges.amount), 0)
        ).filter(
            Charges.charge_type == "rent",
            Charges.period_start < next_month,
            Charges.period_end >= first_day
        )
        .scalar()
    )

    # Outstanding Balance
    # Subquery: total applied per charge 

    applied_subq = (
        db.session.query(
            Application.charge_id.label("charge_id"),
            func.sum(Application.amount_applied).label("total_applied")
        )
        .group_by(Application.charge_id)
        .subquery()
    )

    total_outstanding = (
        db.session.query(
            func.coalesce(
                func.sum(
                    Charges.amount - func.coalesce(applied_subq.c.total_applied, 0)
                ),
                0
            )
        )
        .outerjoin(
            applied_subq,
            applied_subq.c.charge_id == Charges.charge_id
        )
        .filter(
            Charges.status.notin_(["paid", "void"]),
            Charges.due_date <= today
        )
        .scalar()
    )
    
    total_outstanding = 0

    is_under_collected = rent_collected < rent_due
    has_outstanding_balance = total_outstanding > 0

    if not property_obj:
        abort(404)

    return render_template('property_details.html',
                           buildings= buildings_obj,
                           unit_occupied_count=unit_occupied_count,
                           total_units=total_units,
                           rent_collected=rent_collected,
                           rent_due=rent_due,
                           is_under_collected=is_under_collected,
                           total_outstanding=total_outstanding,
                           has_outstanding_balance=has_outstanding_balance,
                           page_title= property_obj.property_name)

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.route('/payments')
def payments():
    return render_template('payments.html', page_title="Payments")

@main.route('/tenants')
def tenants():
    return render_template('tenants.html', page_title="Tenants")
