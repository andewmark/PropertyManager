from flask import Blueprint, render_template
from sqlalchemy import func
from datetime import date
from .models import Property, Unit, Tenant, Lease
from .dummy_data import generate_dummy_properties
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return render_template('dashboard.html', page_title="Dashboard")

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
    
    # TODO: Remove Fallback once DB is Implemented
    if not properties:
        dummy_props, dummy_tenants, dummy_leases = generate_dummy_properties()
        results = [(p, len(p.units)) for p in dummy_props]

    return render_template('properties.html', 
                           prop=results, 
                           page_title="Properties")

@main.route('/properties/<int:property_id>')
def property_detail(property_id):
    property_obj = Property.query.get(property_id)

    today = date.today()
    
    # TODO: Remove Fallback once DB is Implemented
    if not property_obj:
        dummy_props, dummy_tenants, dummy_leases = generate_dummy_properties()
        dummy_map = {p.id: p for p in dummy_props}
        property_obj = dummy_map.get(property_id)

        occupied_count = 0
        for unit in property_obj.units:
            lease = getattr(unit, 'lease', None)
            if lease and lease.start_date <= today <= lease.end_date:
                # optional: ignore if cease_date is set
                if not getattr(lease, 'cease_date', None):
                    occupied_count += 1
    else:
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
