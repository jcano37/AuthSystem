from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: Annotated[str, Field(min_length=8)]
    full_name: str
    is_superuser: bool = False
    is_active: bool = True


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[Annotated[str, Field(min_length=8)]] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class TokenRefresh(BaseModel):
    refresh_token: str


# Password reset schemas
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: Annotated[str, Field(min_length=8)]


# Statistics schemas
class ActiveUsersStats(BaseModel):
    active_sessions_24h: int
    active_users_24h: int
    total_active_sessions: int
    total_users: int
    new_users_7d: int
