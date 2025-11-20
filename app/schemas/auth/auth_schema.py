from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.base import BaseSchema
from app.schemas.users.user_schema import UserResponse


class PasswordResetRequest(BaseSchema):
    email: EmailStr


class PasswordResetConfirm(BaseSchema):
    new_password: str
    access_token: str


class ChangePasswordRequest(BaseSchema):
    current_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserResponse] = None


class RegisterUser(BaseSchema):
    name: str
    email: EmailStr
    phone: str
    password: str
