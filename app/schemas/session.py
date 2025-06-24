from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Session schemas
class UserSessionBase(BaseModel):
    device_info: Optional[str] = None
    ip_address: Optional[str] = None


class UserSessionSchema(UserSessionBase):
    id: int
    user_id: int
    created_at: datetime
    expires_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
