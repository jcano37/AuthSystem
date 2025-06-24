from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


# Properties to receive on item creation
class CompanyCreate(CompanyBase):
    pass


# Properties to receive on item update
class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


# Properties shared by models stored in DB
class CompanyInDBBase(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_root: bool

    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Company(CompanyInDBBase):
    pass
