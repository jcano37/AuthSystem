from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app import crud
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

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
