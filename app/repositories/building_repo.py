from typing import Optional, Any
from app.extensions import db
from sqlalchemy import distinct
from app.models import Building, Maintenance, Documents, DocumentTypes


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
