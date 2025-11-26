from .models import Property, Unit, Tenant, Lease
from datetime import date, timedelta

def generate_dummy_properties():
    # --- Properties ---
    p1 = Property(id=1, name="Elm Street Apartments", address="123 Elm St, Syracuse, NY", image="images/default_property.jpg")
    p2 = Property(id=2, name="Sunset Villas", address="45 Pine Rd, Syracuse, NY")
    p3 = Property(id=3, name="Oak Grove Duplex", address="88 Oak Grove Dr, Syracuse NY")

    # --- Units ---
    u1 = Unit(id=101, unit_number="A1", property=p1)
    u2 = Unit(id=102, unit_number="A2", property=p1)
    u3 = Unit(id=201, unit_number="1A", property=p2)
    u4 = Unit(id=301, unit_number="Unit 1", property=p3)
    u5 = Unit(id=302, unit_number="Unit 2", property=p3)

    p1.units = [u1, u2]
    p2.units = [u3]
    p3.units = [u4, u5]

    # --- Tenants ---
    t1 = Tenant(id=1, tenant_name="Alice Johnson")
    t2 = Tenant(id=2, tenant_name="Bob Smith")
    t3 = Tenant(id=3, tenant_name="Charlie Brown")

    # --- Leases ---
    today = date.today()
    l1 = Lease(id=1, tenant=t1, unit=u1, start_date=today - timedelta(days=60), end_date=today + timedelta(days=300), cease_date=today - timedelta(days=300))
    l2 = Lease(id=2, tenant=t2, unit=u3, start_date=today - timedelta(days=90), end_date=today + timedelta(days=270))
    l3 = Lease(id=3, tenant=t3, unit=u5, start_date=today - timedelta(days=30), end_date=today + timedelta(days=330))

    # Assign leases to units and tenants
    u1.lease = l1
    u3.lease = l2
    u5.lease = l3

    t1.lease = l1
    t2.lease = l2
    t3.lease = l3

    return [p1, p2, p3], [t1, t2, t3], [l1, l2, l3]