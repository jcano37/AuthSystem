from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.redis import add_to_blacklist
from app.core.utils import get_user_by_email_or_username, create_user_from_schema
from app.models.user import User, Session as UserSession
from app.schemas.user import Token, UserCreate, User as UserSchema
from app.core.security import verify_password

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = get_user_by_email_or_username(db, form_data.username, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create session
    access_token = security.create_access_token(user.id)
    refresh_token = security.create_refresh_token(user.id)

    session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        device_info="Web",  # You can enhance this with actual device info
        ip_address="127.0.0.1",  # You can enhance this with actual IP
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/register", response_model=UserSchema)
def register(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    try:
        return create_user_from_schema(db, user_in, is_active=True, is_superuser=user_in.is_superuser)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/refresh", response_model=Token)
def refresh_token(
        *,
        db: Session = Depends(deps.get_db),
        refresh_token: str,
) -> Any:
    """
    Refresh access token
    """
    try:
        payload = security.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # Verify session exists and is valid
        session = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.refresh_token == refresh_token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        ).first()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # Create new tokens
        access_token = security.create_access_token(user_id)
        new_refresh_token = security.create_refresh_token(user_id)

        # Update session
        session.refresh_token = new_refresh_token
        session.expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router.post("/logout")
def logout(
        current_user: User = Depends(deps.get_current_user),
        db: Session = Depends(deps.get_db),
        token: str = Depends(deps.reusable_oauth2),
) -> Any:
    """
    Logout user and invalidate current session
    """
    # Add current access token to blacklist
    payload = security.verify_token(token)
    if payload:
        exp = payload.get("exp")
        if exp:
            ttl = exp - int(datetime.utcnow().timestamp())
            if ttl > 0:
                add_to_blacklist(token, ttl)

    # Invalidate current session
    session = db.query(UserSession).filter(
        UserSession.user_id == current_user.id,
        UserSession.is_active == True
    ).first()

    if session:
        session.is_active = False
        db.commit()

    return {"message": "Successfully logged out"}
