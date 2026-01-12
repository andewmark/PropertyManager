from app.extensions import db

class Property(db.Model):
    __tablename__ = "tbl_property"

    property_id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(100), nullable=False)
    multi_unit = db.Column(db.Boolean, nullable=False)

    buildings = db.relationship("Building", back_populates="property", cascade="all, delete-orphan")


class Address(db.Model):
    __tablename__ = "tbl_address"

    address_id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(500), nullable=False)

    buildings = db.relationship("Building", back_populates="address")


class BuildingType(db.Model):
    __tablename__ = "tbl_building_type"

    building_type_id = db.Column(db.Integer, primary_key=True)
    building_type = db.Column(db.String(50), nullable=False)

    buildings = db.relationship("Building", back_populates="building_type")


class Building(db.Model):
    __tablename__ = "tbl_building"

    building_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("tbl_property.property_id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("tbl_address.address_id"), nullable=False)
    building_name = db.Column(db.String(150), nullable=False)
    building_type_id = db.Column(db.Integer, db.ForeignKey("tbl_building_type.building_type_id"), nullable=False)
    is_main_building = db.Column(db.Boolean, default=False, nullable=False)

    property = db.relationship("Property", back_populates="buildings")
    address = db.relationship("Address", back_populates="buildings")
    building_type = db.relationship("BuildingType", back_populates="buildings")

    units = db.relationship("Unit", back_populates="building", cascade="all, delete-orphan")


class Unit(db.Model):
    __tablename__ = "tbl_units"

    unit_id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("tbl_building.building_id"), nullable=False)
    unit_number = db.Column(db.String(15), nullable=True)
    square_feet = db.Column(db.Integer, nullable=False)
    beds = db.Column(db.Integer, nullable=False)
    baths = db.Column(db.Integer, nullable=False)

    building = db.relationship("Building", back_populates="units")

    lease = db.relationship("Lease", back_populates="unit", cascade="all, delete-orphan")

class Lease(db.Model):
    __tablename__ = "tbl_lease"

    lease_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tbl_tenants.tenant_id"), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    move_out_date = db.Column(db.Date, nullable=True)
    rent = db.Column(db.Numeric(10,2), nullable=False)
    security_deposit = db.Column(db.Numeric(10,2), nullable=False)

    unit = db.relationship("Unit", back_populates="lease")
    tenant = db.relationship("Tenants", back_populates="lease")

    payment = db.relationship("Payments", back_populates="lease", cascade="all, delete-orphan")
    charge = db.relationship("Charges", back_populates="lease", cascade="all, delete-orphan")

class Tenants(db.Model):
    __tablename__ = "tbl_tenants"

    tenant_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    middle_name = db.Column(db.String(150), nullable=True)
    family_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(260), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    emergency_contact_first_name = db.Column(db.String(150), nullable=False)
    emergency_contact_middle_Initial = db.Column(db.String(1), nullable=True)
    emergency_contact_family_name = db.Column(db.String(150), nullable=False)

    lease = db.relationship("Lease", back_populates="tenant", cascade="all, delete-orphan")


class Payments(db.Model):
    __tablename__ = "tbl_payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey("tbl_lease.lease_id"), nullable=False)
    payment_amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    payment_status = db.Column(db.String, nullable=False)

    lease = db.relationship("Lease", back_populates="payment")

    application = db.relationship("Application", back_populates="payment", cascade="all, delete-orphan")

class Charges(db.Model):
    __tablename__ = "tbl_charges"

    charge_id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey("tbl_lease.lease_id"), nullable=False)
    charge_type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    period_start = db.Column(db.Date, nullable=True)
    period_end = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=False)

    lease = db.relationship("Lease", back_populates="charge")

    application = db.relationship("Application", back_populates="charge", cascade="all, delete-orphan")

class Application(db.Model):
    __tablename__ = "tbl_payment_applications"

    application_id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey("tbl_payments.payment_id"), nullable=False)
    charge_id = db.Column(db.Integer, db.ForeignKey("tbl_charges.charge_id"), nullable=False)
    amount_applied = db.Column(db.Numeric(10,2), nullable=False)
    created_at = db.Column(db.DateTime)

    payment = db.relationship("Payments", back_populates="application")
    charge = db.relationship("Charges", back_populates="application")
    
