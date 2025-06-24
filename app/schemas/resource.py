from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResourceTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class ResourceTypeCreate(ResourceTypeBase):
    pass


class ResourceTypeUpdate(ResourceTypeBase):
    name: Optional[str] = None


class ResourceType(ResourceTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
