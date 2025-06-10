from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud
from app.api import deps
from app.models.user import Permission
from app.schemas.user import Permission as PermissionSchema, PermissionCreate, PermissionUpdate

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
    return crud.permission.create_permission(db, permission_in=permission_in)


@router.get("/{permission_id}", response_model=PermissionSchema)
def read_permission(
        *,
        permission: Permission = Depends(deps.get_permission_by_id_from_path),
) -> Any:
    """
    Get permission by ID.
    """
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
    return crud.permission.update_permission(db, db_obj=permission, obj_in=permission_in)


@router.delete("/{permission_id}", response_model=PermissionSchema)
def delete_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission: Permission = Depends(deps.get_permission_by_id_from_path),
) -> Any:
    """
    Delete a permission.
    """
    crud.permission.delete_permission(db, permission_id=permission.id)
    return permission
