from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


def get_user_by_email_or_username(db: Session, email: str, username: str) -> Optional[User]:
    """
    Get user by email or username
    """
    return db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()


def check_user_exists(db: Session, email: str, username: str) -> None:
    """
    Check if user exists and raise appropriate exception
    """
    user = get_user_by_email_or_username(db, email, username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email or username already exists in the system.",
        )


def update_user_data(user: User, user_in: UserUpdate) -> None:
    """
    Update user data from UserUpdate schema
    """
    if user_in.password is not None:
        user.hashed_password = get_password_hash(user_in.password)
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    if user_in.is_superuser is not None:
        user.is_superuser = user_in.is_superuser


def create_user_from_schema(db: Session, user_in: UserCreate, is_active: bool = True,
                            is_superuser: bool = False) -> User:
    """
    Create a new user from UserCreate schema
    """
    # Check if user with email or username already exists
    existing_user = get_user_by_email_or_username(db, user_in.email, user_in.username)
    if existing_user:
        if existing_user.email == user_in.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
    
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=is_active,
        is_superuser=is_superuser,
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        error_detail = "Registration failed"
        if "ix_users_email" in str(e):
            error_detail = "Email already registered"
        elif "ix_users_username" in str(e):
            error_detail = "Username already taken"
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )
