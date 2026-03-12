from app.repositories.unit_repo import (
    get_unit_by_id,
    get_occupied_unit_ids,
    get_current_lease_by_unit_id,
    get_unit_YTD_payments,
    get_unit_YTD_expenses,
    get_outstanding_by_unit_ids,
    get_unit_amenities,
)
from app.repositories.lease_repo import get_lease_by_id
from app.utils.breadcrumbs import generate_breadcrumbs
from app.repositories.building_repo import get_building_by_id


def get_unit_dashboard(unit_id, tab):
    # Validate Parameters
    if unit_id == 0:
        raise ValueError("Unit ID Required")

    # Retrieve Tab Query from URL
    tenants = []
    leases = []
    documents = []

    if tab == "tenants":
        tenants = "tenants"

    # Retrieve Unit Object
    unit_obj = get_unit_by_id(unit_id)
    building_id = unit_obj.building_id

    # Retrieve Building Object
    building_obj = get_building_by_id(building_id)
    property_id = building_obj.property_id

    # Retrieve Lease Object
    lease_ids = get_current_lease_by_unit_id(unit_id)
    lease_ids = [row.lease_id for row in lease_ids]

    # Generate breadcrumb
    breadcrumb = generate_breadcrumbs(property_id, building_id, unit_id)

    # Check if the Unit has an active lease
    occupied = False
    occupied_set = get_occupied_unit_ids([unit_id])
    if len(occupied_set) == 1:
        occupied = True
    elif len(occupied_set) == 0:
        occupied = False
    else:
        raise ValueError(
            f"occupied_set should only have 1 result from unit_id: {unit_id}"
        )

    # Retrieve Current Lease Objects
    leases = []
    if lease_ids:
        for lease_id in lease_ids:
            lease_obj = get_lease_by_id(lease_id)
            leases.append(lease_obj)

    # Calculate total Rent
    # Calculate total Security Deposits
    total_rent = 0
    total_security_deposits = 0
    if leases:
        for lease in leases:
            total_rent += lease.rent
            total_security_deposits += lease.security_deposit

    # Retrieve YTD Payments
    YTD_revenues = get_unit_YTD_payments(unit_id)
    if not YTD_revenues:
        YTD_revenues = 0

    # Retrieve YTD Expenses
    YTD_expenses = get_unit_YTD_expenses(unit_id)
    if not YTD_expenses:
        YTD_expenses = 0

    # Retrieve Outstanding Balance
    outstanding_balance = 0
    outstanding_dict = get_outstanding_by_unit_ids([unit_id])
    if outstanding_dict:
        outstanding_balance = outstanding_dict[unit_id]

    # Retrieve Amenities
    amenities = get_unit_amenities(unit_id)

    return {
        "unit": unit_obj,
        "tab": tab,
        "breadcrumb": breadcrumb,
        "occupied": occupied,
        "leases": leases,
        "total_rent": f"{total_rent:.2f}",
        "total_security_deposits": f"{total_security_deposits:.2f}",
        "YTD_revenues": f"{YTD_revenues:.2f}",
        "YTD_expenses": f"{YTD_expenses:.2f}",
        "outstanding_balance": f"{outstanding_balance:.2f}",
        "amenities": amenities,
    }
