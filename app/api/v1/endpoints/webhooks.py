from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.middlewares.api_auth import require_api_key
from app.models.integration import Integration

router = APIRouter()


@router.post("/{integration_type}")
async def receive_webhook(
    integration_type: str,
    request: Request,
    integration: Integration = Depends(require_api_key),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Endpoint for receiving webhooks from external systems.
    Requires a valid API key in the X-API-Key header.
    """
    # Verify that the integration type matches
    if integration.integration_type != integration_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This endpoint is for {integration_type} integrations only",
        )

    try:
        # Parse the webhook payload
        payload = await request.json()

        # Process the webhook based on integration type
        # This is where you would implement specific logic for each integration type
        result = process_webhook(integration_type, payload, integration, db)

        return {
            "status": "success",
            "message": f"Webhook received for {integration_type}",
            "data": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing webhook: {str(e)}",
        )


def process_webhook(
    integration_type: str,
    payload: Dict[str, Any],
    integration: Integration,
    db: Session,
) -> Dict[str, Any]:
    """
    Process webhook payload based on integration type.
    This function can be expanded to handle different integration types.
    """
    # Example implementation - extend this with specific logic for each integration type
    if integration_type == "oauth2":
        # Process OAuth2 webhook
        return {"processed": True, "type": "oauth2"}
    elif integration_type == "api_key":
        # Process API key webhook
        return {"processed": True, "type": "api_key"}
    else:
        # Generic processing for other types
        return {"processed": True, "type": integration_type}
