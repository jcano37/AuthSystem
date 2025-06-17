from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.models.permissions import Permission
from app.models.roles import Role
from app.schemas.role import RoleCreate, RoleUpdate


def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()


def get_role(db: Session, role_id: int) -> Optional[Role]:
    return (
        db.query(Role)
        .options(selectinload(Role.permissions).selectinload(Permission.resource_type))
        .filter(Role.id == role_id)
        .first()
    )


def get_roles(
    db: Session, skip: int = 0, limit: int = 100, include_permissions: bool = True
) -> List[Role]:
    query = db.query(Role)
    if include_permissions:
        query = query.options(
            selectinload(Role.permissions).selectinload(Permission.resource_type)
        )
    return query.offset(skip).limit(limit).all()


def create_role(db: Session, *, role_in: RoleCreate) -> Role:
    if get_role_by_name(db, name=role_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The role with this name already exists in the system.",
        )
    db_obj = Role(**role_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_role(db: Session, *, db_obj: Role, obj_in: RoleUpdate) -> Role:
    update_data = obj_in.dict(exclude_unset=True)

    if "name" in update_data and update_data["name"] != db_obj.name:
        if get_role_by_name(db, name=update_data["name"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The role with this name already exists in the system.",
            )

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_role(db: Session, *, role_id: int) -> Optional[Role]:
    role = get_role(db, role_id)
    if role:
        db.delete(role)
        db.commit()
    return role


def assign_permission_to_role(
    db: Session, *, role: Role, permission: Permission
) -> Role:
    if permission in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission is already assigned to this role",
        )
    role.permissions.append(permission)
    db.commit()
    db.refresh(role)
    return role


def remove_permission_from_role(
    db: Session, *, role: Role, permission: Permission
) -> Role:
    if permission not in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission is not assigned to this role",
        )
    role.permissions.remove(permission)
    db.commit()
    db.refresh(role)
    return role
