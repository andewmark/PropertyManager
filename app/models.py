from app.extensions import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200))

    unit = db.relationship('Unit', back_populates='property', cascade="all, delete-orphan")

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_number = db.Column(db.String(10), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

    leases = db.relationship('Lease', back_populates='unit', cascade="all, delete-orphan")
    property = db.relationship('Property', back_populates='unit',)

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    leases = db.relationship('Lease', back_populates='tenant', cascade="all, delete-orphan")

class Lease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    cease_date = db.Column(db.Date, nullable=True)
    rent = db.Column(db.Float, nullable=False)

    unit = db.relationship('Unit', back_populates='leases')
    tenant = db.relationship('Tenant', back_populates='leases')

