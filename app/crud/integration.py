import secrets
import string
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.integration import Integration
from app.schemas.integration import IntegrationCreate, IntegrationUpdate


def generate_api_credentials():
    """Generate secure API key and secret"""
    alphabet = string.ascii_letters + string.digits
    api_key = "".join(secrets.choice(alphabet) for _ in range(32))
    api_secret = "".join(secrets.choice(alphabet) for _ in range(64))
    return api_key, api_secret


def get_integration(db: Session, integration_id: int) -> Optional[Integration]:
    """Get integration by ID"""
    return db.query(Integration).filter(Integration.id == integration_id).first()


def get_integration_by_api_key(db: Session, api_key: str) -> Optional[Integration]:
    """Get integration by API key"""
    return db.query(Integration).filter(Integration.api_key == api_key).first()


def get_integrations(
    db: Session, company_id: int, skip: int = 0, limit: int = 100
) -> List[Integration]:
    """Get all integrations for a company"""
    return (
        db.query(Integration)
        .filter(Integration.company_id == company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_integration(
    db: Session, *, integration_in: IntegrationCreate, company_id: int
) -> Integration:
    """Create a new integration"""
    api_key, api_secret = generate_api_credentials()

    db_obj = Integration(
        **integration_in.model_dump(),
        api_key=api_key,
        api_secret=api_secret,
        company_id=company_id,
        is_active=True,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_integration(
    db: Session, *, db_obj: Integration, obj_in: IntegrationUpdate | Dict[str, Any]
) -> Integration:
    """Update integration"""
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)

    for field in update_data:
        setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_integration(db: Session, *, integration_id: int) -> Optional[Integration]:
    """Delete an integration"""
    integration = get_integration(db, integration_id=integration_id)
    if integration:
        db.delete(integration)
        db.commit()
    return integration


def regenerate_api_secret(db: Session, *, db_obj: Integration) -> Integration:
    """Regenerate API secret for an integration"""
    _, api_secret = generate_api_credentials()
    db_obj.api_secret = api_secret
    db_obj.updated_at = datetime.now(timezone.utc)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
