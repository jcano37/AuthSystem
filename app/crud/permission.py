from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.user import Permission
from app.schemas.user import PermissionCreate, PermissionUpdate


def get_permission_by_name(db: Session, name: str) -> Optional[Permission]:
    return db.query(Permission).filter(Permission.name == name).first()


def get_permission(db: Session, permission_id: int) -> Optional[Permission]:
    return (
        db.query(Permission)
        .options(joinedload(Permission.resource_type))
        .filter(Permission.id == permission_id)
        .first()
    )


def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
    return (
        db.query(Permission)
        .options(joinedload(Permission.resource_type))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_permission(db: Session, *, permission_in: PermissionCreate) -> Permission:
    if get_permission_by_name(db, name=permission_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The permission with this name already exists in the system.",
        )
    db_obj = Permission(**permission_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # Load the resource_type relationship
    db.refresh(db_obj, ["resource_type"])
    return db_obj


def update_permission(
    db: Session, *, db_obj: Permission, obj_in: PermissionUpdate
) -> Permission:
    update_data = obj_in.dict(exclude_unset=True)

    if "name" in update_data and update_data["name"] != db_obj.name:
        if get_permission_by_name(db, name=update_data["name"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The permission with this name already exists in the system.",
            )

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # Load the resource_type relationship
    db.refresh(db_obj, ["resource_type"])
    return db_obj


def delete_permission(db: Session, *, permission_id: int) -> Optional[Permission]:
    permission = get_permission(db, permission_id)
    if permission:
        db.delete(permission)
        db.commit()
    return permission
