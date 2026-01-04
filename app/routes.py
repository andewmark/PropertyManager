from flask import Blueprint, render_template
from sqlalchemy import func
from datetime import date
from app.models import Property, Unit, Tenant, Lease
from app.extensions import db
from sqlalchemy import text

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
    # For now, fake data if DB is empty:
    properties = Property.query.all()

    results = (
        db.session.query(
            Property,
            func.count(Unit.id).label("unit_count")
        )
        .outerjoin(Unit)
        .group_by(Property.id)
        .all()
    )

    return render_template('properties.html', 
                           prop=results, 
                           page_title="Properties")

@main.route('/properties/<int:property_id>')
def property_detail(property_id):
    property_obj = Property.query.get(property_id)

    today = date.today()
    
 
    occupied_count = (
        db.session.query(Unit)
        .join(Lease)
        .filter(
            Unit.property_id == property_id,
            Lease.start_date <= today,
            Lease.end_date >= today,
            Lease.cease_date == None  # optional
        )
        .count()
    )

    if not property_obj:
        return "Property not found", 404
    
    return render_template('property_details.html',
                           prop=property_obj,
                           page_title=property_obj.name,
                           occupied_units=occupied_count)

@main.route('/payments')
def payments():
    return render_template('payments.html', page_title="Payments")

@main.route('/tenants')
def tenants():
    return render_template('tenants.html', page_title="Tenants")
