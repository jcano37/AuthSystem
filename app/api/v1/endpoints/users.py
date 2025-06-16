from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta
from app.api import deps
from app import crud
from app.models.user import User, Session as UserSession
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate, UserSessionSchema, ActiveUsersStats
from app.core.redis import add_to_blacklist
from app.core import security

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_user_me(
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserUpdate,
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = crud.user.update_user(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me/sessions", response_model=List[UserSessionSchema])
def get_my_sessions(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user's active sessions.
    """
    sessions = db.query(UserSession).filter(
        and_(
            UserSession.user_id == current_user.id,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        )
    ).order_by(UserSession.created_at.desc()).all()
    
    return sessions


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
    session = db.query(UserSession).filter(
        and_(
            UserSession.id == session_id,
            UserSession.user_id == current_user.id,
            UserSession.is_active == True
        )
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Deactivate session
    session.is_active = False
    
    # Add refresh token to blacklist
    payload = security.verify_token(session.refresh_token)
    if payload:
        exp = payload.get("exp")
        if exp:
            ttl = exp - int(datetime.utcnow().timestamp())
            if ttl > 0:
                add_to_blacklist(session.refresh_token, ttl)
    
    db.commit()
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
        current_session = db.query(UserSession).filter(
            and_(
                UserSession.user_id == current_user.id,
                UserSession.is_active == True
            )
        ).first()
    
    # Get all active sessions
    sessions = db.query(UserSession).filter(
        and_(
            UserSession.user_id == current_user.id,
            UserSession.is_active == True
        )
    ).all()
    
    revoked_count = 0
    for session in sessions:
        # Skip current session
        if current_session and session.id == current_session.id:
            continue
            
        session.is_active = False
        
        # Add refresh token to blacklist
        payload = security.verify_token(session.refresh_token)
        if payload:
            exp = payload.get("exp")
            if exp:
                ttl = exp - int(datetime.utcnow().timestamp())
                if ttl > 0:
                    add_to_blacklist(session.refresh_token, ttl)
        
        revoked_count += 1
    
    db.commit()
    return {"message": f"Revoked {revoked_count} sessions successfully"}


@router.get("/active-stats", response_model=ActiveUsersStats)
def get_active_users_stats(
        *,
        db: Session = Depends(deps.get_db),
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get statistics about active users and sessions.
    """
    # Active sessions in last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    
    active_sessions_24h = db.query(UserSession).filter(
        and_(
            UserSession.is_active == True,
            UserSession.created_at >= last_24h,
            UserSession.expires_at > datetime.utcnow()
        )
    ).count()
    
    # Unique active users in last 24 hours
    active_users_24h = db.query(func.count(func.distinct(UserSession.user_id))).filter(
        and_(
            UserSession.is_active == True,
            UserSession.created_at >= last_24h,
            UserSession.expires_at > datetime.utcnow()
        )
    ).scalar()
    
    # Total active sessions
    total_active_sessions = db.query(UserSession).filter(
        and_(
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        )
    ).count()
    
    # Total users
    total_users = db.query(User).filter(User.is_active == True).count()
    
    # Users registered in last 7 days
    last_7d = datetime.utcnow() - timedelta(days=7)
    new_users_7d = db.query(User).filter(
        User.created_at >= last_7d
    ).count()
    
    return {
        "active_sessions_24h": active_sessions_24h,
        "active_users_24h": active_users_24h or 0,
        "total_active_sessions": total_active_sessions,
        "total_users": total_users,
        "new_users_7d": new_users_7d
    }


@router.get("/active-sessions", response_model=List[UserSessionSchema])
def get_active_sessions(
        *,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get all active sessions (admin only).
    """
    sessions = db.query(UserSession).filter(
        and_(
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        )
    ).order_by(UserSession.created_at.desc()).offset(skip).limit(limit).all()
    
    return sessions


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
    session = db.query(UserSession).filter(
        and_(
            UserSession.id == session_id,
            UserSession.is_active == True
        )
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Deactivate session
    session.is_active = False
    
    # Add refresh token to blacklist
    payload = security.verify_token(session.refresh_token)
    if payload:
        exp = payload.get("exp")
        if exp:
            ttl = exp - int(datetime.utcnow().timestamp())
            if ttl > 0:
                add_to_blacklist(session.refresh_token, ttl)
    
    db.commit()
    return {"message": "Session revoked successfully"}


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
        user: User = Depends(deps.get_user_by_id_from_path),
) -> Any:
    """
    Get a specific user by id.
    """
    return user


@router.get("/", response_model=List[UserSchema])
def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserCreate,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    return crud.user.create_user(db, user_in=user_in)


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserUpdate,
        user: User = Depends(deps.get_user_by_id_from_path),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.update_user(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
        *,
        db: Session = Depends(deps.get_db),
        user: User = Depends(deps.get_user_by_id_from_path),
) -> Any:
    """
    Delete a user.
    """
    crud.user.delete_user(db, user_id=user.id)
    return user
