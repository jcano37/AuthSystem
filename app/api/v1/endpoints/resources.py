from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.resource import ResourceType
from app.schemas.resource import ResourceType as ResourceTypeSchema
from app.schemas.resource import ResourceTypeCreate, ResourceTypeUpdate

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
    resource_types = crud.resource.get_resource_types(db, skip=skip, limit=limit)
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
    return crud.resource.create_resource_type(db, resource_type_in=resource_type_in)


@router.put("/{resource_type_id}", response_model=ResourceTypeSchema)
def update_resource_type(
    *,
    db: Session = Depends(deps.get_db),
    resource_type_in: ResourceTypeUpdate,
    resource_type: ResourceType = Depends(deps.get_resource_type_by_id_from_path),
) -> Any:
    """
    Update a resource type.
    """
    return crud.resource.update_resource_type(
        db, db_obj=resource_type, obj_in=resource_type_in
    )


@router.delete("/{resource_type_id}", response_model=ResourceTypeSchema)
def delete_resource_type(
    *,
    db: Session = Depends(deps.get_db),
    resource_type: ResourceType = Depends(deps.get_resource_type_by_id_from_path),
) -> Any:
    """
    Delete a resource type.
    """
    return crud.resource.delete_resource_type(db, resource_type_id=resource_type.id)
