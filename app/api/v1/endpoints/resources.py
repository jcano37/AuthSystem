from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.resource import ResourceType
from app.schemas.resource import ResourceType as ResourceTypeSchema, ResourceTypeCreate, ResourceTypeUpdate

router = APIRouter()


@router.get("/", response_model=List[ResourceTypeSchema])
def read_resource_types(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        _: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve resource types.
    """
    resource_types = db.query(ResourceType).offset(skip).limit(limit).all()
    return resource_types


@router.post("/", response_model=ResourceTypeSchema)
def create_resource_type(
        *,
        db: Session = Depends(deps.get_db),
        resource_type_in: ResourceTypeCreate,
        _: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new resource type.
    """
    # Check if resource type with the same name already exists
    existing_resource_type = db.query(ResourceType).filter(ResourceType.name == resource_type_in.name).first()
    if existing_resource_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resource type with name '{resource_type_in.name}' already exists"
        )

    resource_type = ResourceType(
        name=resource_type_in.name,
        description=resource_type_in.description,
    )
    db.add(resource_type)
    db.commit()
    db.refresh(resource_type)
    return resource_type


@router.put("/{resource_type_id}", response_model=ResourceTypeSchema)
def update_resource_type(
        *,
        db: Session = Depends(deps.get_db),
        resource_type_id: int,
        resource_type_in: ResourceTypeUpdate,
        _: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a resource type.
    """
    resource_type = db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()
    if not resource_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource type not found",
        )
    
    # Check if new name exists and is different from current name
    if resource_type_in.name is not None and resource_type_in.name != resource_type.name:
        existing_resource_type = db.query(ResourceType).filter(
            ResourceType.name == resource_type_in.name,
            ResourceType.id != resource_type_id
        ).first()
        if existing_resource_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Resource type with name '{resource_type_in.name}' already exists"
            )
    
    if resource_type_in.name is not None:
        resource_type.name = resource_type_in.name
    if resource_type_in.description is not None:
        resource_type.description = resource_type_in.description
    
    db.add(resource_type)
    db.commit()
    db.refresh(resource_type)
    return resource_type


@router.delete("/{resource_type_id}", response_model=ResourceTypeSchema)
def delete_resource_type(
        *,
        db: Session = Depends(deps.get_db),
        resource_type_id: int,
        _: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a resource type.
    """
    resource_type = db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()
    if not resource_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource type not found",
        )
    
    # Check if there are any permissions associated with this resource type
    if resource_type.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete resource type that has associated permissions. Please delete or reassign the permissions first."
        )
    
    db.delete(resource_type)
    db.commit()
    return resource_type
