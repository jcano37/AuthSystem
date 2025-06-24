from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.integration import Integration

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_integration_from_api_key(
    request: Request,
    api_key: str = Depends(api_key_header),
    db: Session = Depends(deps.get_db),
) -> Optional[Integration]:
    """
    Dependency to get integration from API key.
    Returns None if no API key is provided or if the API key is invalid.
    """
    if not api_key:
        return None

    integration = crud.integration.get_integration_by_api_key(db, api_key=api_key)

    if integration and integration.is_active:
        # Store integration and company_id in request state for later use
        request.state.integration = integration
        request.state.company_id = integration.company_id
        return integration

    return None


async def require_api_key(
    integration: Optional[Integration] = Depends(get_integration_from_api_key),
) -> Integration:
    """
    Dependency to require a valid API key.
    Raises 401 if no API key is provided or if the API key is invalid.
    """
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return integration
