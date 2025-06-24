from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.permission import Permission


# Role schemas
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    created_at: datetime
    is_default: Optional[bool] = False
    updated_at: Optional[datetime] = None
    company_id: int

    model_config = ConfigDict(from_attributes=True)


# Role with permissions schema
class RoleWithPermissions(Role):
    permissions: List[Permission] = []
