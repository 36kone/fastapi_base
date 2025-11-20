from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, ConfigDict

from app.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id: UUID
    name: str
    email: EmailStr
    phone: str
    role: str
    password: str
    password_recovery: str
    password_recovery_expire: datetime
    is_active: bool


class CreateUser(BaseSchema):
    name: str
    email: EmailStr
    phone: str
    role: str = "user"
    password: str


class UpdateUser(BaseSchema):
    id: UUID
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    password_recovery: Optional[str] = None
    password_recovery_expire: Optional[datetime] = None
    is_active: Optional[bool] = None


class UserResponse(BaseSchema):
    id: UUID
    name: str
    email: EmailStr
    phone: str
    role: str
    password_recovery: Optional[str] = None
    password_recovery_expire: Optional[datetime] = None
    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserSearchRequest(BaseSchema):
    keyword: Optional[str] = None
    size: int = 10
    page: int = 1
