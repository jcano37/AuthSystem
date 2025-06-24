from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class IntegrationBase(BaseModel):
    name: str
    description: Optional[str] = None
    integration_type: str
    callback_url: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None


# Properties to receive on item creation
class IntegrationCreate(IntegrationBase):
    pass


# Properties to receive on item update
class IntegrationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    callback_url: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


# Properties shared by models stored in DB
class IntegrationInDBBase(IntegrationBase):
    id: int
    api_key: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    company_id: int

    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Integration(IntegrationInDBBase):
    pass


# Additional properties stored in DB, not returned to client
class IntegrationInDB(IntegrationInDBBase):
    api_secret: str
