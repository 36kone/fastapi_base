from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    id: UUID
    name: str
    email: str
    password: str


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    id: UUID
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
