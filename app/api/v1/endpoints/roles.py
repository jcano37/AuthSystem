from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import Role, Permission, User
from app.schemas.user import Role as RoleSchema, RoleCreate, RoleUpdate
from app.schemas.user import Permission as PermissionSchema, PermissionCreate, PermissionUpdate

router = APIRouter()


# Role endpoints
@router.get("/", response_model=List[RoleSchema])
def read_roles(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve roles.
    """
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.post("/", response_model=RoleSchema)
def create_role(
        *,
        db: Session = Depends(deps.get_db),
        role_in: RoleCreate,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new role.
    """
    role = db.query(Role).filter(Role.name == role_in.name).first()
    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The role with this name already exists in the system.",
        )
    role = Role(**role_in.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.put("/{role_id}", response_model=RoleSchema)
def update_role(
        *,
        db: Session = Depends(deps.get_db),
        role_id: int,
        role_in: RoleUpdate,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    for field, value in role_in.dict(exclude_unset=True).items():
        setattr(role, field, value)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{role_id}", response_model=RoleSchema)
def delete_role(
        *,
        db: Session = Depends(deps.get_db),
        role_id: int,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    db.delete(role)
    db.commit()
    return role


# Permission endpoints
@router.get("/permissions", response_model=List[PermissionSchema])
def read_permissions(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve permissions.
    """
    permissions = db.query(Permission).offset(skip).limit(limit).all()
    return permissions


@router.post("/permissions", response_model=PermissionSchema)
def create_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_in: PermissionCreate,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new permission.
    """
    permission = db.query(Permission).filter(Permission.name == permission_in.name).first()
    if permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The permission with this name already exists in the system.",
        )
    permission = Permission(**permission_in.dict())
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@router.put("/permissions/{permission_id}", response_model=PermissionSchema)
def update_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_id: int,
        permission_in: PermissionUpdate,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a permission.
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    for field, value in permission_in.dict(exclude_unset=True).items():
        setattr(permission, field, value)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@router.delete("/permissions/{permission_id}", response_model=PermissionSchema)
def delete_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_id: int,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a permission.
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    db.delete(permission)
    db.commit()
    return permission
