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
