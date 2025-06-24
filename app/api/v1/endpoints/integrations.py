from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.integration import Integration as IntegrationSchema
from app.schemas.integration import IntegrationCreate, IntegrationUpdate

router = APIRouter()


@router.get("/", response_model=List[IntegrationSchema])
def get_integrations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve integrations for the current user's company.
    """
    integrations = crud.integration.get_integrations(
        db, company_id=current_user.company_id, skip=skip, limit=limit
    )
    return integrations


@router.post("/", response_model=IntegrationSchema)
def create_integration(
    *,
    db: Session = Depends(deps.get_db),
    integration_in: IntegrationCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new integration.
    Only superusers can create integrations.
    """
    integration = crud.integration.create_integration(
        db=db, integration_in=integration_in, company_id=current_user.company_id
    )
    return integration


@router.get("/{integration_id}", response_model=IntegrationSchema)
def get_integration(
    *,
    db: Session = Depends(deps.get_db),
    integration_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get integration by ID.
    """
    integration = crud.integration.get_integration(db, integration_id=integration_id)

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found",
        )

    # Check if integration belongs to user's company
    if (
        integration.company_id != current_user.company_id
        and not current_user.is_superuser
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this integration",
        )

    return integration


@router.put("/{integration_id}", response_model=IntegrationSchema)
def update_integration(
    *,
    db: Session = Depends(deps.get_db),
    integration_id: int,
    integration_in: IntegrationUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update integration.
    Only superusers can update integrations.
    """
    integration = crud.integration.get_integration(db, integration_id=integration_id)

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found",
        )

    # Check if integration belongs to user's company
    if (
        integration.company_id != current_user.company_id
        and not current_user.is_superuser
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this integration",
        )

    integration = crud.integration.update_integration(
        db=db, db_obj=integration, obj_in=integration_in
    )
    return integration


@router.delete("/{integration_id}", response_model=IntegrationSchema)
def delete_integration(
    *,
    db: Session = Depends(deps.get_db),
    integration_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete integration.
    Only superusers can delete integrations.
    """
    integration = crud.integration.get_integration(db, integration_id=integration_id)

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found",
        )

    # Check if integration belongs to user's company
    if (
        integration.company_id != current_user.company_id
        and not current_user.is_superuser
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this integration",
        )

    integration = crud.integration.delete_integration(db, integration_id=integration_id)
    return integration


@router.post("/{integration_id}/regenerate-secret", response_model=IntegrationSchema)
def regenerate_api_secret(
    *,
    db: Session = Depends(deps.get_db),
    integration_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Regenerate API secret for an integration.
    Only superusers can regenerate API secrets.
    """
    integration = crud.integration.get_integration(db, integration_id=integration_id)

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found",
        )

    # Check if integration belongs to user's company
    if (
        integration.company_id != current_user.company_id
        and not current_user.is_superuser
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this integration",
        )

    integration = crud.integration.regenerate_api_secret(db, db_obj=integration)
    return integration
