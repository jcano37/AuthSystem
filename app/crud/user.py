import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

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


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, *, user_in: UserCreate) -> User:
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

    db_obj = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
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
        update_data = obj_in.dict(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

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
