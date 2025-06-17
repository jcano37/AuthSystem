from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Permission schemas
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    resource_type_id: int
    action: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    resource: Optional[str] = None  # This will be populated from resource_type.name

    class Config:
        from_attributes = True
