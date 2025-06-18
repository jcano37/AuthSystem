import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import PasswordResetToken, User
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_by_email_or_username(
    db: Session, *, email: str, username: str
) -> Optional[User]:
    return (
        db.query(User)
        .filter((User.email == email) | (User.username == username))
        .first()
    )


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[User] = None,
) -> List[User]:
    """
    Get users based on user permissions
    - Superusers from root company see all users
    - Superusers from other companies see only users in their company
    - Regular users see only themselves
    """
    query = db.query(User)

    # If no current user specified, return all users (admin endpoint)
    if not current_user:
        return query.offset(skip).limit(limit).all()

    # Current user is provided
    if current_user.is_superuser:
        # Check if user is from root company
        from app.crud.company import get_root_company

        root_company = get_root_company(db)

        if current_user.company_id != root_company.id:
            # Non-root superusers can only see users from their company
            query = query.filter(User.company_id == current_user.company_id)
    else:
        # Regular users can only see themselves
        query = query.filter(User.id == current_user.id)

    return query.offset(skip).limit(limit).all()


def create_user(
    db: Session, *, user_in: UserCreate, company_id: Optional[int] = None
) -> User:
    """Create a new user with company consideration"""
    # Check if email/username already exists
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    if get_user_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    # Use provided company_id if available, otherwise use the one from input
    final_company_id = company_id if company_id is not None else user_in.company_id

    user_data = user_in.model_dump(exclude={"password"})
    user_data["hashed_password"] = get_password_hash(user_in.password)
    user_data["company_id"] = final_company_id

    db_obj = User(**user_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_user(
    db: Session, *, db_obj: User, obj_in: UserUpdate | Dict[str, Any]
) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    # Prevent changing company_id unless explicitly needed
    if "company_id" in update_data:
        # This should be handled with special permissions in the API
        pass

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_user(db: Session, *, user_id: int) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


def create_password_reset_token(db: Session, *, user: User) -> PasswordResetToken:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(
        hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS
    )
    db_token = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_password_reset_token_by_token(
    db: Session, *, token: str
) -> Optional[PasswordResetToken]:
    return (
        db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    )


def reset_password(
    db: Session, *, token_obj: PasswordResetToken, new_password: str
) -> None:
    if token_obj.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has already been used",
        )
    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
        )

    user = get_user_by_id(db, user_id=token_obj.user_id)
    if not user:
        # This should not happen if the token is valid, but as a safeguard
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    token_obj.is_used = True
    db.add(user)
    db.add(token_obj)
    db.commit()
