from typing import Optional, Any
from datetime import date
from app.extensions import db
from sqlalchemy import distinct, func, literal, null
from app.models import (
    Building,
    Maintenance,
    Documents,
    DocumentTypes,
    MaintenanceType,
    Unit,
    Charges,
    Payments,
    Application,
    Tenants,
    Lease,
    PropertyExpenses,
)


def get_building_by_id(building_id: int) -> Optional[Building]:
    return Building.query.get(building_id)


def get_building_by_id_and_property(
    building_id: int, property_id: int
) -> Optional[Building]:
    return Building.query.filter_by(
        building_id=building_id, property_id=property_id
    ).first()


def get_active_building_maintenance(building_id: int) -> int:
    return (
        db.session.query(distinct(Maintenance.maintenance_id))
        .filter(Maintenance.building_id == building_id)
        .filter(Maintenance.date_completed.is_(None))
        .count()
    )


def get_building_documents(building_id: int) -> list[Any]:
    return (
        db.session.query(
            Documents.stored_filename,
            DocumentTypes.document_type,
            Documents.uploaded_at,
        )
        .join(Documents, Documents.document_type_id == DocumentTypes.document_type_id)
        .filter(Documents.building_id == building_id)
        .all()
    )


def get_building_maintenance(building_id: int) -> list[Any]:
    """
    Query for maintenance related to passed in building

    Args:
        building_id (int)

    Returns:
        list[Any]:
    """
    return (
        db.session.query(
            Maintenance.maintenance_id,
            MaintenanceType.maintenance_type,
            Maintenance.unit_id,
            Unit.unit_number,
            Maintenance.date_requested,
            Maintenance.status,
            Maintenance.priority,
        )
        .join(
            MaintenanceType,
            MaintenanceType.maintenance_type_id == Maintenance.maintenance_type_id,
        )
        .outerjoin(Unit, Maintenance.unit_id == Unit.unit_id)
        .filter(Maintenance.building_id == building_id)
        .all()
    )


def get_building_transactions(building_id: int) -> list[Any]:
    """
    Returns combined list of charges and expenses for a building's transactions table,
    normalized into a shared structure
    """
    charges = (
        db.session.query(
            literal("charge").label("transaction_type"),
            Charges.charge_type.label("description"),
            Unit.unit_id,
            Unit.unit_number,
            Payments.payment_date.label("date"),
            Application.amount_applied.label("amount"),
            func.concat(Tenants.first_name, " ", Tenants.family_name).label(
                "tenant_name"
            ),
        )
        .join(Payments, Payments.payment_id == Application.payment_id)
        .join(Charges, Charges.charge_id == Application.charge_id)
        .join(Lease, Lease.lease_id == Charges.lease_id)
        .join(Tenants, Tenants.tenant_id == Lease.tenant_id)
        .join(Unit, Unit.unit_id == Lease.unit_id)
        .filter(Unit.building_id == building_id)
    )

    expenses = (
        db.session.query(
            literal("expense").label("transaction_type"),
            PropertyExpenses.description.label("description"),
            PropertyExpenses.unit_id,
            Unit.unit_number,
            PropertyExpenses.date_incurred.label("date"),
            PropertyExpenses.expense_amount.label("amount"),
            null().label("tenant_name"),
        )
        .outerjoin(Unit, PropertyExpenses.unit_id == Unit.unit_id)
        .filter(PropertyExpenses.building_id == building_id)
    )

    return charges.union_all(expenses).order_by("date").all()


def get_building_expiring_leases(building_id: int, today: date) -> list[Any]:
    """
    Args:
        building_id (int)

    Returns:
        list[Any]: Returns Expiring leases
    """
    return (
        db.session.query(
            func.concat(Tenants.first_name, " ", Tenants.family_name).label(
                "tenant_name"
            ),
            Unit.unit_number,
            Lease.end_date,
        )
        .join(Unit, Unit.unit_id == Lease.unit_id)
        .join(Tenants, Tenants.tenant_id == Lease.tenant_id)
        .filter(Lease.end_date >= today)
        .filter(Unit.building_id == building_id)
        .order_by(Lease.end_date.desc())
        .limit(4)
        .all()
    )
