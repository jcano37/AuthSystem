from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import Role, Permission, User, role_permission
from app.schemas.user import Role as RoleSchema, RoleCreate, RoleUpdate, RoleWithPermissions
from app.schemas.user import Permission as PermissionSchema

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


@router.get("/{role_id}", response_model=RoleWithPermissions)
def read_role(
        *,
        db: Session = Depends(deps.get_db),
        role_id: int,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get role by ID with permissions.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return role


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
    
    # Si se está cambiando el nombre, verificar que no exista otro rol con ese nombre
    if role_in.name and role_in.name != role.name:
        existing_role = db.query(Role).filter(Role.name == role_in.name).first()
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The role with this name already exists in the system.",
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


@router.post("/{role_id}/permissions/{permission_id}", response_model=RoleWithPermissions)
def assign_permission_to_role(
        *,
        db: Session = Depends(deps.get_db),
        role_id: int,
        permission_id: int,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Assign a permission to a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    
    # Check if the permission is already assigned to the role
    if permission in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission is already assigned to this role",
        )
    
    role.permissions.append(permission)
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{role_id}/permissions/{permission_id}", response_model=RoleWithPermissions)
def remove_permission_from_role(
        *,
        db: Session = Depends(deps.get_db),
        role_id: int,
        permission_id: int,
        _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Remove a permission from a role.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    
    # Check if the permission is assigned to the role
    if permission not in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission is not assigned to this role",
        )
    
    role.permissions.remove(permission)
    db.commit()
    db.refresh(role)
    return role
