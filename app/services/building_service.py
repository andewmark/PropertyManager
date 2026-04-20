from typing import Any
from decimal import Decimal

from app.repositories.property_repo import get_property_by_id
from app.utils.dates import current_month_bounds
from app.repositories.building_repo import (
    get_building_by_id_and_property,
    get_active_building_maintenance,
    get_building_documents,
    get_building_maintenance,
    get_building_transactions,
    get_building_expiring_leases,
)
from app.repositories.unit_repo import (
    get_occupied_unit_ids,
    get_current_tenants_by_unit_ids,
    get_current_rent_by_unit_ids,
    get_outstanding_by_unit_ids,
)
from app.repositories.finance_repo import (
    get_rent_collected_by_building,
    get_rent_due_by_building,
    get_building_next_rent_due_date,
    get_total_outstanding_for_building,
)

from app.utils.breadcrumbs import generate_breadcrumbs


def get_building_dashboard(
    property_id: int, building_id: int, tab: str
) -> dict[str, Any] | None:
    property_obj = get_property_by_id(property_id)
    building_obj = get_building_by_id_and_property(building_id, property_id)

    if not property_obj or not building_obj:
        return None

    # Initialize variables
    charges_total = 0
    expenses_total = 0
    net_total = 0

    today, first_day, next_month = current_month_bounds()
    breadcrumb = generate_breadcrumbs(property_id=property_id, building_id=building_id)

    units = building_obj.units
    unit_ids = [unit.unit_id for unit in units]  # type: ignore

    occupied_unit_ids = get_occupied_unit_ids(unit_ids)

    # Retrieve Tab Query from URL
    units_data = []
    maintenance = []
    documents = []
    transactions = []

    if tab == "units":
        # Retrieve per Unit data
        tenants_by_unit = get_current_tenants_by_unit_ids(unit_ids)
        rent_by_unit = get_current_rent_by_unit_ids(unit_ids)
        outstanding_by_unit = get_outstanding_by_unit_ids(unit_ids)

        for unit in units:  # type: ignore
            units_data.append(
                {
                    "unit": unit,
                    "is_occupied": unit.unit_id in occupied_unit_ids,
                    "tenants": tenants_by_unit.get(unit.unit_id, []),
                    "current_rent": rent_by_unit.get(unit.unit_id),
                    "outstanding_balance": outstanding_by_unit.get(unit.unit_id),
                }
            )
    elif tab == "maintenance":
        maintenance = get_building_maintenance(building_id)
        open_maintenance = len(maintenance)
    elif tab == "documents":
        documents = get_building_documents(building_id)
    elif tab == "transactions":
        transactions = get_building_transactions(building_id)
        charges_total = sum(
            t.amount for t in transactions if t.transaction_type == "charge"
        )
        expenses_total = sum(
            t.amount for t in transactions if t.transaction_type == "expense"
        )
        net_total = charges_total - expenses_total

    # Calculate Occupancy Rate
    unit_occupied_count = len(occupied_unit_ids)
    total_units = len(unit_ids)
    occupancy_rate = (int)((unit_occupied_count / total_units) * 100)

    # Retrieve Rent Collected Vs. Expected
    rent_collected = get_rent_collected_by_building(first_day, next_month, building_id)
    rent_due = get_rent_due_by_building(first_day, next_month, building_id)
    next_rent_due = get_building_next_rent_due_date(first_day, next_month, building_id)

    # Retrieve Total Outstanding balance
    total_outstanding = get_total_outstanding_for_building(today, building_id)

    # Retrieve Open Work orders
    if tab != "maintenance":
        open_maintenance = get_active_building_maintenance(building_id)

    # Retrieve upcoming Lease expirations
    expiring_leases = get_building_expiring_leases(building_id, today)
    expiring_leases_data = [
        {
            "tenant_name": lease.tenant_name,
            "unit_number": lease.unit_number,
            "end_date": lease.end_date,
            "days_until_expiry": (lease.end_date - today).days,
        }
        for lease in expiring_leases
    ]

    # Retrieve Delinquency Breakdown

    return {
        "building": building_obj,
        "units": units_data,
        "unit_occupied_count": unit_occupied_count,
        "total_units": total_units,
        "occupancy_rate": occupancy_rate,
        "rent_collected": rent_collected,
        "rent_due": rent_due,
        "is_under_collected": (rent_collected or Decimal(0)) < (rent_due or Decimal(0)),
        "total_outstanding": total_outstanding,
        "next_rent_due": next_rent_due,
        "breadcrumb": breadcrumb,
        "open_maintenance": open_maintenance,  # type: ignore
        "tab": tab,
        "maintenance": maintenance,
        "documents": documents,
        "transactions": transactions,
        "charges_total": charges_total,
        "expenses_total": expenses_total,
        "net_total": net_total,
        "expiring_leases": expiring_leases_data,
    }
