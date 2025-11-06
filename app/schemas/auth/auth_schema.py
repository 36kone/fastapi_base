from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.users.user_schema import UserResponse


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    new_password: str
    access_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserResponse] = None
