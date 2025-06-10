from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import Permission, User
from app.schemas.user import Permission as PermissionSchema, PermissionCreate, PermissionUpdate

router = APIRouter()


@router.get("/", response_model=List[PermissionSchema])
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


@router.post("/", response_model=PermissionSchema)
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
    permission = Permission(
        name=permission_in.name,
        description=permission_in.description,
        resource_type_id=permission_in.resource_type_id,
        action=permission_in.action
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@router.get("/{permission_id}", response_model=PermissionSchema)
def read_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_id: int,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get permission by ID.
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    return permission


@router.put("/{permission_id}", response_model=PermissionSchema)
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
    
    # Si se está cambiando el nombre, verificar que no exista otro permiso con ese nombre
    if permission_in.name and permission_in.name != permission.name:
        existing_permission = db.query(Permission).filter(Permission.name == permission_in.name).first()
        if existing_permission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The permission with this name already exists in the system.",
            )
    
    update_data = permission_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(permission, field, update_data[field])
    
    # Validar que el tipo de recurso exista
    if 'resource_type_id' in update_data:
        from app.models.resource import ResourceType
        resource_type = db.query(ResourceType).filter(ResourceType.id == update_data['resource_type_id']).first()
        if not resource_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Resource type with id {update_data['resource_type_id']} not found"
            )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@router.delete("/{permission_id}", response_model=PermissionSchema)
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