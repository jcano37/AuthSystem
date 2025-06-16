from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.resource import ResourceType
from app.schemas.resource import ResourceTypeCreate, ResourceTypeUpdate


def get_resource_types(
    db: Session, skip: int = 0, limit: int = 100
) -> List[ResourceType]:
    return db.query(ResourceType).offset(skip).limit(limit).all()


def get_resource_type(db: Session, resource_type_id: int) -> Optional[ResourceType]:
    return db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()


def get_resource_type_by_name(db: Session, *, name: str) -> Optional[ResourceType]:
    return db.query(ResourceType).filter(ResourceType.name == name).first()


def create_resource_type(
    db: Session, *, resource_type_in: ResourceTypeCreate
) -> ResourceType:
    if get_resource_type_by_name(db, name=resource_type_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resource type with name '{resource_type_in.name}' already exists",
        )

    db_obj = ResourceType(
        name=resource_type_in.name,
        description=resource_type_in.description,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_resource_type(
    db: Session, *, db_obj: ResourceType, obj_in: ResourceTypeUpdate
) -> ResourceType:
    update_data = obj_in.dict(exclude_unset=True)

    if "name" in update_data and update_data["name"] != db_obj.name:
        if get_resource_type_by_name(db, name=update_data["name"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Resource type with name '{update_data['name']}' already exists",
            )

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_resource_type(db: Session, *, resource_type_id: int) -> ResourceType:
    resource_type = get_resource_type(db, resource_type_id)
    if not resource_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource type not found",
        )

    if resource_type.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete resource type that has associated permissions. Please delete or reassign the permissions first.",
        )

    db.delete(resource_type)
    db.commit()
    return resource_type
