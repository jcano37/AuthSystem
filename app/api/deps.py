from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.redis import is_blacklisted
from app.core.security import verify_token
from app.db.session import SessionLocal
from app.models.company import Company
from app.models.permissions import Permission
from app.models.resource import ResourceType
from app.models.roles import Role
from app.models.user import User
from app.schemas.user import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        # Check if token is blacklisted
        if is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenPayload(**payload)

        if token_data.type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


def check_permissions(required_permissions: list[str]):
    def permission_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_permissions = []
        for role in current_user.roles:
            # Check if role belongs to user's company
            if role.company_id == current_user.company_id:
                for permission in role.permissions:
                    user_permissions.append(permission.name)

        # Superusers in root company have all permissions
        if current_user.is_superuser:
            root_company = crud.company.get_root_company(db=SessionLocal())
            if current_user.company_id == root_company.id:
                return current_user

        if not all(perm in user_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return current_user

    return permission_checker


def get_user_by_id_from_path(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    user = crud.user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    # Check if user belongs to same company or is superuser
    if user.company_id != current_user.company_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user


def get_permission_by_id_from_path(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Permission:
    permission = crud.permission.get_permission(db, permission_id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    return permission


def get_role_by_id_from_path(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Role:
    role = crud.role.get_role(db, role_id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    # Check if role belongs to same company or is superuser
    if role.company_id != current_user.company_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return role


def get_resource_type_by_id_from_path(
    resource_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ResourceType:
    resource_type = crud.resource.get_resource_type(
        db, resource_type_id=resource_type_id
    )
    if not resource_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource type not found",
        )
    # Check if resource type belongs to same company or is superuser
    if (
        resource_type.company_id != current_user.company_id
        and not current_user.is_superuser
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return resource_type


def get_company_by_id_from_path(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Company:
    company = crud.company.get_company_by_id(db, company_id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    # Regular users can only access their own company
    if company.id != current_user.company_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return company
