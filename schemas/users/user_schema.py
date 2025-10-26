from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)