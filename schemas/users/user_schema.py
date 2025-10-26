from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    role: str
    password: str
    password_recovery: str
    password_recovery_expire: datetime
    is_active: bool


class CreateUser(BaseModel):
    name: str
    email: str
    phone: str
    role: str
    password: str
    is_active: bool


class UpdateUser(BaseModel):
    id: UUID
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    password_recovery: Optional[str] = None
    password_recovery_expire: Optional[datetime] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    role: str
    password_recovery: Optional[str] = None
    password_recovery_expire: Optional[datetime] = None
    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
