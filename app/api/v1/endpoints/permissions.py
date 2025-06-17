from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.permissions import Permission
from app.schemas.permission import Permission as PermissionSchema
from app.schemas.permission import PermissionCreate, PermissionUpdate

router = APIRouter()


@router.get("/", response_model=List[PermissionSchema])
def read_permissions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    _=Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve permissions.
    """
    permissions = crud.permission.get_permissions(db, skip=skip, limit=limit)
    # Add resource name to each permission
    for permission in permissions:
        if permission.resource_type:
            permission.resource = permission.resource_type.name
    return permissions


@router.post("/", response_model=PermissionSchema)
def create_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_in: PermissionCreate,
    _=Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new permission.
    """
    permission = crud.permission.create_permission(db, permission_in=permission_in)
    if permission.resource_type:
        permission.resource = permission.resource_type.name
    return permission


@router.get("/{permission_id}", response_model=PermissionSchema)
def read_permission(
    *,
    permission: Permission = Depends(deps.get_permission_by_id_from_path),
) -> Any:
    """
    Get permission by ID.
    """
    if permission.resource_type:
        permission.resource = permission.resource_type.name
    return permission


@router.put("/{permission_id}", response_model=PermissionSchema)
def update_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_in: PermissionUpdate,
    permission: Permission = Depends(deps.get_permission_by_id_from_path),
) -> Any:
    """
    Update a permission.
    """
    updated_permission = crud.permission.update_permission(
        db, db_obj=permission, obj_in=permission_in
    )
    if updated_permission.resource_type:
        updated_permission.resource = updated_permission.resource_type.name
    return updated_permission


@router.delete("/{permission_id}", response_model=PermissionSchema)
def delete_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission: Permission = Depends(deps.get_permission_by_id_from_path),
) -> Any:
    """
    Delete a permission.
    """
    if permission.resource_type:
        permission.resource = permission.resource_type.name
    crud.permission.delete_permission(db, permission_id=permission.id)
    return permission
