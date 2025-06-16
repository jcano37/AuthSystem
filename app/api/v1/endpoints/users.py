from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.session import UserSessionSchema
from app.schemas.user import ActiveUsersStats
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate

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


@router.get("/active-stats", response_model=ActiveUsersStats)
def get_active_users_stats(
    *,
    db: Session = Depends(deps.get_db),
    _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get statistics about active users and sessions.
    """
    # Get session statistics from CRUD
    session_stats = crud.session.get_session_statistics(db)

    # Total users
    total_users = db.query(User).filter(User.is_active == True).count()

    # Users registered in last 7 days
    from datetime import datetime

    last_7d = datetime.utcnow() - timedelta(days=7)
    new_users_7d = db.query(User).filter(User.created_at >= last_7d).count()

    return {
        "active_sessions_24h": session_stats["active_sessions_24h"],
        "active_users_24h": session_stats["active_users_24h"],
        "total_active_sessions": session_stats["total_active_sessions"],
        "total_users": total_users,
        "new_users_7d": new_users_7d,
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
    return crud.session.get_all_active_sessions(db, skip=skip, limit=limit)


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
