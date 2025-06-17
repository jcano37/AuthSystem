from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.permissions import Permission
from app.models.roles import Role
from app.models.user import User
from app.schemas.role import Role as RoleSchema
from app.schemas.role import RoleCreate, RoleUpdate, RoleWithPermissions

router = APIRouter()


# Role endpoints
@router.get("/")
def read_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    include_permissions: bool = True,
    _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve roles with optional permissions.
    """
    roles = crud.role.get_roles(
        db, skip=skip, limit=limit, include_permissions=include_permissions
    )

    if include_permissions:
        # Return roles with permissions
        result = []
        for role in roles:
            # Try to validate with more explicit conversion
            validated_role = RoleWithPermissions.model_validate(
                {
                    **role.__dict__,
                    "permissions": [
                        {**p.__dict__, "name": p.name} for p in role.permissions
                    ],
                }
            )
            result.append(validated_role)
        return result
    else:
        # Return roles without permissions
        return [RoleSchema.model_validate(role) for role in roles]


@router.get("/{role_id}", response_model=RoleWithPermissions)
def read_role(
    *,
    role: Role = Depends(deps.get_role_by_id_from_path),
) -> Any:
    """
    Get role by ID with permissions.
    """
    return role


@router.post("/", response_model=RoleSchema)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: RoleCreate,
    _=Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new role.
    """
    return crud.role.create_role(db, role_in=role_in)


@router.put("/{role_id}", response_model=RoleSchema)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: RoleUpdate,
    role: Role = Depends(deps.get_role_by_id_from_path),
) -> Any:
    """
    Update a role.
    """
    return crud.role.update_role(db, db_obj=role, obj_in=role_in)


@router.delete("/{role_id}", response_model=RoleSchema)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    role: Role = Depends(deps.get_role_by_id_from_path),
) -> Any:
    """
    Delete a role.
    """
    crud.role.delete_role(db, role_id=role.id)
    return role


@router.post(
    "/{role_id}/permissions/{permission_id}", response_model=RoleWithPermissions
)
def assign_permission_to_role(
    *,
    db: Session = Depends(deps.get_db),
    role: Role = Depends(deps.get_role_by_id_from_path),
    permission: Permission = Depends(deps.get_permission_by_id_from_path),
) -> Any:
    """
    Assign a permission to a role.
    """
    return crud.role.assign_permission_to_role(db, role=role, permission=permission)


@router.delete(
    "/{role_id}/permissions/{permission_id}", response_model=RoleWithPermissions
)
def remove_permission_from_role(
    *,
    db: Session = Depends(deps.get_db),
    role: Role = Depends(deps.get_role_by_id_from_path),
    permission: Permission = Depends(deps.get_permission_by_id_from_path),
) -> Any:
    """
    Remove a permission from a role.
    """
    return crud.role.remove_permission_from_role(db, role=role, permission=permission)
