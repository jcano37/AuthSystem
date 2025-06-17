from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.redis import add_to_blacklist
from app.core.security import verify_password
from app.models.sessions import Session as UserSession
from app.models.user import User
from app.schemas.user import PasswordReset, PasswordResetRequest, Token, TokenRefresh
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.get_by_email_or_username(
        db, email=form_data.username, username=form_data.username
    )

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Update last login
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    # Create session
    access_token = security.create_access_token(user.id)
    refresh_token = security.create_refresh_token(user.id)

    session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        device_info=request.headers.get("User-Agent", "Unknown"),
        ip_address=request.client.host,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
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
        user = crud.user.create_user(db, user_in=user_in)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )


@router.post("/refresh", response_model=Token)
def refresh_token(
    *,
    db: Session = Depends(deps.get_db),
    token_data: TokenRefresh,
) -> Any:
    """
    Refresh access token
    """
    try:
        payload = security.verify_token(token_data.refresh_token)
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
        session = crud.session.get_session_by_refresh_token(
            db, user_id=user_id, refresh_token=token_data.refresh_token
        )

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
        session.expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
    except Exception:
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
            ttl = exp - int(datetime.now(timezone.utc).timestamp())
            if ttl > 0:
                add_to_blacklist(token, ttl)

    # Invalidate current session
    session = crud.session.get_user_sessions_for_logout(db, user_id=current_user.id)

    if session:
        crud.session.revoke_session(db, session)

    return {"message": "Successfully logged out"}


@router.post("/password-reset-request", status_code=status.HTTP_202_ACCEPTED)
def request_password_reset(
    *, db: Session = Depends(deps.get_db), password_reset_request: PasswordResetRequest
) -> Any:
    """
    Request password reset. This will trigger an email to be sent to the user.
    """
    user = crud.user.get_user_by_email(db, email=password_reset_request.email)
    if not user:
        # For security, we don't reveal if the user exists or not.
        # We'll just return a 202 Accepted status in any case.
        return {
            "message": "If a matching account exists, an email will be sent with instructions."
        }

    password_reset_token = crud.user.create_password_reset_token(db, user=user)
    # TODO: Send an email to the user with the token.
    # For development, we'll return the token in the response.
    print(f"Password reset token for {user.email}: {password_reset_token.token}")
    return {
        "message": "If a matching account exists, an email will be sent with instructions."
    }


@router.post("/password-reset")
def reset_password(
    *, db: Session = Depends(deps.get_db), password_reset: PasswordReset
) -> Any:
    """
    Reset password using the token from the email.
    """
    token_obj = crud.user.get_password_reset_token_by_token(
        db, token=password_reset.token
    )
    if (
        not token_obj
        or token_obj.is_used
        or token_obj.expires_at < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )

    crud.user.reset_password(
        db, token_obj=token_obj, new_password=password_reset.new_password
    )
    return {"message": "Password updated successfully"}
