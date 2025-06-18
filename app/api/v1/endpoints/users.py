from datetime import datetime, timedelta, timezone
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
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
    # Don't allow changing company through this endpoint
    if hasattr(user_in, "company_id") and user_in.company_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change company through this endpoint",
        )

    user = crud.user.update_user(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/active-stats", response_model=ActiveUsersStats)
def get_active_users_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get statistics about active users and sessions.
    For regular superusers, scoped to their company.
    For root superusers, global stats.
    """
    # Check if user is from root company
    root_company = crud.company.get_root_company(db)
    is_root_user = current_user.company_id == root_company.id

    # Get session statistics from CRUD
    session_stats = crud.session.get_session_statistics(
        db, company_id=None if is_root_user else current_user.company_id
    )

    # Query filters
    query_filters = []
    if not is_root_user:
        query_filters.append(User.company_id == current_user.company_id)

    # Total users
    total_users = db.query(User).filter(User.is_active == True, *query_filters).count()

    # Users registered in last 7 days
    last_7d = datetime.now(timezone.utc) - timedelta(days=7)
    new_users_query = db.query(User).filter(User.created_at >= last_7d, *query_filters)
    new_users_7d = new_users_query.count()

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
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get all active sessions (admin only).
    For regular superusers, scoped to their company.
    For root superusers, all sessions.
    """
    # Check if user is from root company
    root_company = crud.company.get_root_company(db)
    is_root_user = current_user.company_id == root_company.id

    return crud.session.get_all_active_sessions(
        db,
        skip=skip,
        limit=limit,
        company_id=None if is_root_user else current_user.company_id,
    )


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
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users based on the user's permissions:
    - Root superusers see all users
    - Company superusers see their company's users
    - Regular users see only themselves
    """
    users = crud.user.get_users(db, skip=skip, limit=limit, current_user=current_user)
    return users


@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    For regular superusers, only in their own company.
    For root superusers, in any company.
    """
    # Check if user is from root company
    root_company = crud.company.get_root_company(db)
    is_root_user = current_user.company_id == root_company.id

    # Non-root superusers can only create users in their own company
    if not is_root_user and user_in.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create users in your own company",
        )

    # Check if target company exists
    target_company = crud.company.get_company_by_id(db, company_id=user_in.company_id)
    if not target_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {user_in.company_id} not found",
        )

    return crud.user.create_user(db, user_in=user_in)


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    user: User = Depends(deps.get_user_by_id_from_path),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    - Root superusers can change any user
    - Company superusers can only update users in their company
    """
    # Check if user is from root company
    root_company = crud.company.get_root_company(db)
    is_root_user = current_user.company_id == root_company.id

    # Check if trying to change company
    if user_in.company_id is not None:
        # Only root users can change company
        if not is_root_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only root superusers can change a user's company",
            )

        # Check if target company exists
        target_company = crud.company.get_company_by_id(
            db, company_id=user_in.company_id
        )
        if not target_company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with id {user_in.company_id} not found",
            )

    user = crud.user.update_user(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_user_by_id_from_path),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    - Root superusers can delete any user except root
    - Company superusers can only delete in their company
    """
    # Prevent deleting root user
    root_company = crud.company.get_root_company(db)

    if user.is_superuser and user.company_id == root_company.id:
        # Check if this is the only root superuser
        root_superusers = (
            db.query(User)
            .filter(User.is_superuser == True, User.company_id == root_company.id)
            .count()
        )

        if root_superusers <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete the only root superuser",
            )

    user = crud.user.delete_user(db, user_id=user.id)
    return user
