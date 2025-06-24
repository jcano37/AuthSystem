from datetime import datetime, timezone
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.core import security
from app.core.redis import add_to_blacklist
from app.models.user import User
from app.schemas.session import UserSessionSchema

router = APIRouter()


@router.get("/me/sessions", response_model=List[UserSessionSchema])
def get_my_sessions(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user's active sessions.
    """
    return crud.session.get_user_active_sessions(db, user_id=current_user.id)


@router.delete("/me/sessions/{session_id}")
def revoke_session(
    *,
    db: Session = Depends(deps.get_db),
    session_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Revoke a specific session.
    """
    session = crud.session.get_user_session_by_id(
        db, user_id=current_user.id, session_id=session_id
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    # Add refresh token to blacklist
    payload = security.verify_token(session.refresh_token)
    if payload:
        exp = payload.get("exp")
        if exp:
            ttl = exp - int(datetime.now(timezone.utc).timestamp())
            if ttl > 0:
                add_to_blacklist(session.refresh_token, ttl)

    # Revoke session using CRUD
    crud.session.revoke_session(db, session)
    return {"message": "Session revoked successfully"}


@router.delete("/me/sessions")
def revoke_all_sessions(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    token: str = Depends(deps.reusable_oauth2),
) -> Any:
    """
    Revoke all user sessions except current one.
    """
    # Get current session to exclude it
    current_payload = security.verify_token(token)
    current_session = None

    if current_payload:
        current_session = crud.session.get_current_user_session(
            db, user_id=current_user.id
        )

    # Get all active sessions
    sessions = crud.session.get_user_active_sessions(db, user_id=current_user.id)

    revoked_count = 0
    for session in sessions:
        # Skip current session
        if current_session and session.id == current_session.id:
            continue

        # Add refresh token to blacklist
        payload = security.verify_token(session.refresh_token)
        if payload:
            exp = payload.get("exp")
            if exp:
                ttl = exp - int(datetime.now(timezone.utc).timestamp())
                if ttl > 0:
                    add_to_blacklist(session.refresh_token, ttl)

        # Revoke session using CRUD
        crud.session.revoke_session(db, session)
        revoked_count += 1

    return {"message": f"Revoked {revoked_count} sessions successfully"}


@router.delete("/sessions/{session_id}")
def admin_revoke_session(
    *,
    db: Session = Depends(deps.get_db),
    session_id: int,
    _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Revoke any session (admin only).
    """
    session = crud.session.get_session_by_id(db, session_id=session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    # Add refresh token to blacklist
    payload = security.verify_token(session.refresh_token)
    if payload:
        exp = payload.get("exp")
        if exp:
            ttl = exp - int(datetime.now(timezone.utc).timestamp())
            if ttl > 0:
                add_to_blacklist(session.refresh_token, ttl)

    # Revoke session using CRUD
    crud.session.revoke_session(db, session)
    return {"message": "Session revoked successfully"}
