from typing import Optional

from app.models import Lease


def get_lease_by_id(lease_id: int) -> Optional[Lease]:
    return Lease.query.get(lease_id)
