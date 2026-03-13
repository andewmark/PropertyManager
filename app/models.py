from __future__ import annotations

from app.extensions import db
from sqlalchemy.orm import Mapped, relationship

from decimal import Decimal


class Property(db.Model):
    __tablename__ = "tbl_property"

    property_id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    property_name: Mapped[str] = db.Column(db.String(100), nullable=False)
    multi_unit: Mapped[bool] = db.Column(db.Boolean, nullable=False)

    buildings = db.relationship(
        "Building", back_populates="property", cascade="all, delete-orphan"
    )
    recurring_expenses = db.relationship(
        "RecurringExpenses", back_populates="property", cascade="all, delete-orphan"
    )
    image = db.relationship(
        "Images", back_populates="property", cascade="all, delete-orphan"
    )
    documents = db.relationship(
        "Documents", back_populates="property", cascade="all, delete-orphan"
    )
    property_expense = db.relationship(
        "PropertyExpenses", back_populates="property", cascade="all, delete-orphan"
    )


class Address(db.Model):
    __tablename__ = "tbl_address"

    address_id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    street_number: Mapped[str] = db.Column(db.String(10), nullable=False)
    city: Mapped[str] = db.Column(db.String(200), nullable=False)
    state: Mapped[str | None] = db.Column(db.String(50), nullable=True)
    postal_code: Mapped[str] = db.Column(db.String(10), nullable=False)
    country: Mapped[str] = db.Column(db.String(50), nullable=False)
    street: Mapped[str] = db.Column(db.String(500), nullable=False)

    buildings = db.relationship("Building", back_populates="address")


class BuildingType(db.Model):
    __tablename__ = "tbl_building_type"

    building_type_id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    building_type: Mapped[str] = db.Column(db.String(50), nullable=False)

    buildings = db.relationship("Building", back_populates="building_type")


class Building(db.Model):
    __tablename__ = "tbl_building"

    building_id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    property_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("tbl_property.property_id"), nullable=False
    )
    address_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("tbl_address.address_id"), nullable=False
    )
    building_name: Mapped[str] = db.Column(db.String(150), nullable=False)
    building_type_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("tbl_building_type.building_type_id"), nullable=False
    )
    is_main_building: Mapped[int] = db.Column(db.Boolean, default=False, nullable=False)

    property = db.relationship("Property", back_populates="buildings")
    address = db.relationship("Address", back_populates="buildings")
    building_type = db.relationship("BuildingType", back_populates="buildings")

    units = db.relationship(
        "Unit", back_populates="building", cascade="all, delete-orphan"
    )
    recurring_expenses = db.relationship(
        "RecurringExpenses", back_populates="building", cascade="all, delete-orphan"
    )
    image = db.relationship(
        "Images", back_populates="building", cascade="all, delete-orphan"
    )
    property_expense = db.relationship(
        "PropertyExpenses", back_populates="building", cascade="all, delete-orphan"
    )


class Unit(db.Model):
    __tablename__ = "tbl_units"

    unit_id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    building_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("tbl_building.building_id"), nullable=False
    )
    unit_number: Mapped[str | None] = db.Column(db.String(15), nullable=True)
    square_feet: Mapped[str] = db.Column(db.Integer, nullable=False)
    beds: Mapped[int] = db.Column(db.Integer, nullable=False)
    baths: Mapped[int] = db.Column(db.Integer, nullable=False)
    market_rent: Mapped[Decimal] = db.Column(db.Numeric(10, 2), nullable=False)

    building = db.relationship("Building", back_populates="units")

    lease = db.relationship(
        "Lease", back_populates="unit", cascade="all, delete-orphan"
    )
    maintenance = db.relationship(
        "Maintenance", back_populates="unit", cascade="all, delete-orphan"
    )
    recurring_expenses = db.relationship(
        "RecurringExpenses", back_populates="unit", cascade="all, delete-orphan"
    )
    image = db.relationship(
        "Images", back_populates="unit", cascade="all, delete-orphan"
    )
    documents = db.relationship(
        "Documents", back_populates="unit", cascade="all, delete-orphan"
    )
    property_expense = db.relationship(
        "PropertyExpenses", back_populates="unit", cascade="all, delete-orphan"
    )
    unit_amenities = db.relationship(
        "UnitAmenities", back_populates="unit", cascade="all, delete-orphan"
    )
    unit_utilities = db.relationship(
        "UnitUtilities", back_populates="unit", cascade="all, delete-orphan"
    )


class Lease(db.Model):
    __tablename__ = "tbl_lease"

    lease_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(
        db.Integer, db.ForeignKey("tbl_tenants.tenant_id"), nullable=False
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    move_out_date = db.Column(db.Date, nullable=True)
    rent = db.Column(db.Numeric(10, 2), nullable=False)
    security_deposit = db.Column(db.Numeric(10, 2), nullable=False)

    unit = db.relationship("Unit", back_populates="lease")
    tenant = db.relationship("Tenants", back_populates="lease")

    payment = db.relationship(
        "Payments", back_populates="lease", cascade="all, delete-orphan"
    )
    charge = db.relationship(
        "Charges", back_populates="lease", cascade="all, delete-orphan"
    )


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
    emergency_contact_phone = db.Column(db.String(15), nullable=True)

    lease = db.relationship(
        "Lease", back_populates="tenant", cascade="all, delete-orphan"
    )
    maintenance = db.relationship(
        "Maintenance", back_populates="tenant", cascade="all, delete-orphan"
    )


class Payments(db.Model):
    __tablename__ = "tbl_payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(
        db.Integer, db.ForeignKey("tbl_lease.lease_id"), nullable=False
    )
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    payment_status = db.Column(db.String, nullable=False)

    lease = db.relationship("Lease", back_populates="payment")

    application = db.relationship(
        "Application", back_populates="payment", cascade="all, delete-orphan"
    )


class Charges(db.Model):
    __tablename__ = "tbl_charges"

    charge_id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(
        db.Integer, db.ForeignKey("tbl_lease.lease_id"), nullable=False
    )
    charge_type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    period_start = db.Column(db.Date, nullable=True)
    period_end = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    lease = db.relationship("Lease", back_populates="charge")

    application = db.relationship(
        "Application", back_populates="charge", cascade="all, delete-orphan"
    )


class Application(db.Model):
    __tablename__ = "tbl_payment_applications"

    application_id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(
        db.Integer, db.ForeignKey("tbl_payments.payment_id"), nullable=False
    )
    charge_id = db.Column(
        db.Integer, db.ForeignKey("tbl_charges.charge_id"), nullable=False
    )
    amount_applied = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime)

    payment = db.relationship("Payments", back_populates="application")
    charge = db.relationship("Charges", back_populates="application")


class Vendors(db.Model):
    __tablename__ = "tbl_vendors"

    vendor_id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String, nullable=False)
    service_type = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String, nullable=True)

    maintenance = db.relationship(
        "Maintenance", back_populates="vendor", cascade="all, delete-orphan"
    )
    recurring_expenses = db.relationship(
        "RecurringExpenses", back_populates="vendor", cascade="all, delete-orphan"
    )
    property_expense = db.relationship(
        "PropertyExpenses", back_populates="vendor", cascade="all, delete-orphan"
    )


class Maintenance(db.Model):
    __tablename__ = "tbl_maintenance"

    request_id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=True)
    tenant_id = db.Column(
        db.Integer, db.ForeignKey("tbl_tenants.tenant_id"), nullable=True
    )
    description = db.Column(db.String(500), nullable=True)
    priority = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    date_requested = db.Column(db.Date, nullable=False)
    date_completed = db.Column(db.Date, nullable=True)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("tbl_vendors.vendor_id"), nullable=True
    )

    vendor = db.relationship("Vendors", back_populates="maintenance")
    tenant = db.relationship("Tenants", back_populates="maintenance")
    unit = db.relationship("Unit", back_populates="maintenance")

    documents = db.relationship(
        "Documents", back_populates="maintenance", cascade="all, delete-orphan"
    )


class ExpenseCategory(db.Model):
    __tablename__ = "tbl_expense_category"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_group = db.Column(db.String(30), nullable=False)

    recurring_expenses = db.relationship(
        "RecurringExpenses",
        back_populates="expense_category",
        cascade="all, delete-orphan",
    )
    property_expense = db.relationship(
        "PropertyExpenses",
        back_populates="expense_category",
        cascade="all, delete-orphan",
    )


class RecurringExpenses(db.Model):
    __tablename__ = "tbl_recurring_expenses"

    recurring_rule_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(
        db.Integer, db.ForeignKey("tbl_property.property_id"), nullable=False
    )
    building_id = db.Column(
        db.Integer, db.ForeignKey("tbl_building.building_id"), nullable=True
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=True)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("tbl_vendors.vendor_id"), nullable=True
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("tbl_expense_category.category_id"), nullable=False
    )
    description = db.Column(db.String(500), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    frequency = db.Column(db.Interval, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    payment_method = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    property = db.relationship("Property", back_populates="recurring_expenses")
    building = db.relationship("Building", back_populates="recurring_expenses")
    unit = db.relationship("Unit", back_populates="recurring_expenses")
    vendor = db.relationship("Vendors", back_populates="recurring_expenses")
    expense_category = db.relationship(
        "ExpenseCategory", back_populates="recurring_expenses"
    )

    property_expense = db.relationship(
        "PropertyExpenses",
        back_populates="recurring_expenses",
        cascade="all, delete-orphan",
    )


class Images(db.Model):
    __tablename__ = "tbl_images"

    image_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(
        db.Integer, db.ForeignKey("tbl_property.property_id"), nullable=False
    )
    building_id = db.Column(
        db.Integer, db.ForeignKey("tbl_building.building_id"), nullable=True
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=True)
    filepath = db.Column(db.String(1000), nullable=False)
    stored_filename = db.Column(db.String(1000), nullable=False)
    original_filename = db.Column(db.String(1000), nullable=False)
    file_type = db.Column(db.String(15), nullable=False)
    file_size = db.Column(db.String(15), nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False)
    display_order = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.Date, nullable=False)

    property = db.relationship("Property", back_populates="image")
    building = db.relationship("Building", back_populates="image")
    unit = db.relationship("Unit", back_populates="image")


class Documents(db.Model):
    __tablename__ = "tbl_documents"

    document_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(
        db.Integer, db.ForeignKey("tbl_property.property_id"), nullable=False
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=True)
    expense_id = db.Column(
        db.Integer, db.ForeignKey("tbl_property_expenses.expense_id")
    )
    request_id = db.Column(
        db.Integer, db.ForeignKey("tbl_maintenance.request_id"), nullable=True
    )
    filepath = db.Column(db.String(1000), nullable=False)
    stored_filename = db.Column(db.String(1000), nullable=False)
    original_filename = db.Column(db.String(1000), nullable=False)
    file_type = db.Column(db.String(15), nullable=False)
    file_size = db.Column(db.String(15), nullable=False)
    storage_location = db.Column(db.String(1000), nullable=False)
    uploaded_at = db.Column(db.Date, nullable=False)
    lease_id = db.Column(db.Integer, db.ForeignKey("tbl_lease.lease_id"), nullable=True)

    property = db.relationship("Property", back_populates="documents")
    unit = db.relationship("Unit", back_populates="documents")
    maintenance = db.relationship("Maintenance", back_populates="documents")
    property_expense = db.relationship("PropertyExpenses", back_populates="documents")


class PropertyExpenses(db.Model):
    __tablename__ = "tbl_property_expenses"

    expense_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(
        db.Integer, db.ForeignKey("tbl_property.property_id"), nullable=False
    )
    building_id = db.Column(
        db.Integer, db.ForeignKey("tbl_building.building_id"), nullable=True
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey("tbl_vendors.vendor_id"))
    expense_category_id = db.Column(
        db.Integer, db.ForeignKey("tbl_expense_category.category_id"), nullable=False
    )
    description = db.Column(db.String(500), nullable=True)
    expense_amount = db.Column(db.Numeric(10, 2), nullable=False)
    date_incurred = db.Column(db.Date, nullable=False)
    date_paid = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String, nullable=True)
    recurring_rule_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_recurring_expenses.recurring_rule_id"),
        nullable=True,
    )

    property = db.relationship("Property", back_populates="property_expense")
    building = db.relationship("Building", back_populates="property_expense")
    unit = db.relationship("Unit", back_populates="property_expense")
    vendor = db.relationship("Vendors", back_populates="property_expense")
    expense_category = db.relationship(
        "ExpenseCategory", back_populates="property_expense"
    )
    recurring_expenses = db.relationship(
        "RecurringExpenses", back_populates="property_expense"
    )

    documents = db.relationship(
        "Documents", back_populates="property_expense", cascade="all, delete-orphan"
    )


class Amenities(db.Model):
    __tablename__ = "tbl_amenities"

    amenity_id = db.Column(db.Integer, primary_key=True)
    amenity_name = db.Column(db.String(100), nullable=False)

    unit_amenities = db.relationship(
        "UnitAmenities", back_populates="amenities", cascade="all, delete-orphan"
    )


class UnitAmenities(db.Model):
    __tablename__ = "tbl_unit_amenities"

    unit_id = db.Column(
        db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=False
    )  # also was pointing to tbl_lease, not tbl_units
    amenity_id = db.Column(
        db.Integer, db.ForeignKey("tbl_amenities.amenity_id"), nullable=False
    )

    __table_args__ = (db.PrimaryKeyConstraint("unit_id", "amenity_id"),)

    unit = db.relationship("Unit", back_populates="unit_amenities")
    amenities = db.relationship("Amenities", back_populates="unit_amenities")


class Utilities(db.Model):
    __tablename__ = "tbl_utilities"

    utility_id = db.Column(db.Integer, primary_key=True)
    utility_name = db.Column(db.String(100), nullable=False)

    unit_utilities = db.relationship(
        "UnitUtilities", back_populates="utilities", cascade="all, delete-orphan"
    )


class UnitUtilities(db.Model):
    __tablename__ = "tbl_unit_utilities"

    unit_id = db.Column(
        db.Integer, db.ForeignKey("tbl_units.unit_id"), nullable=False
    )  # also was pointing to tbl_lease, not tbl_units
    utility_id = db.Column(
        db.Integer, db.ForeignKey("tbl_utilities.utility_id"), nullable=False
    )

    __table_args__ = (db.PrimaryKeyConstraint("unit_id", "utility_id"),)

    unit = db.relationship("Unit", back_populates="unit_utilities")
    utilities = db.relationship("Utilities", back_populates="unit_utilities")
