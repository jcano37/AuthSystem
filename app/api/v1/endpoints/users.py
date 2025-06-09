from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.utils import check_user_exists, update_user_data, create_user_from_schema
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
    update_user_data(current_user, user_in)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
        user_id: int,
        current_user: User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
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
    users = db.query(User).offset(skip).limit(limit).all()
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
    check_user_exists(db, user_in.email, user_in.username)
    return create_user_from_schema(db, user_in)


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: UserUpdate,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    update_user_data(user, user_in)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(user)
    db.commit()
    return user
