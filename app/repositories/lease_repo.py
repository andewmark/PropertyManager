from app.models import Lease


def get_lease_by_id(lease_id):
    return Lease.query.get(lease_id)
