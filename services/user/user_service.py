from typing import Optional
from uuid import UUID

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import get_password_hash
from db.database import get_db
from dependencies.exception_utils import ensure_or_404, ensure_or_400
from models.users.users import User
from schemas import CreateUser, UpdateUser, MessageSchema
from services.crud_service import CrudService


class UserService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.crud_service = CrudService(User, session)

    def create(self, user: CreateUser) -> User:
        entity = User(
            name=user.name,
            email=str(user.email),
            password=get_password_hash(user.password),
            phone=str(user.phone),
            role=user.role,
            is_active=user.is_active,
        )
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def read(self) -> list[User]:
        return self.crud_service.read()

    def get_by_id(self, user_id: UUID) -> User:
        return self.crud_service.get_by_id(user_id)

    def get_by_email(self, email: str) -> User:
        return ensure_or_404(
            self.session.scalar((select(User).where(User.email == email))),
            "User not found",
        )

    def update(self, data: UpdateUser) -> User:
        return self.crud_service.update(data.id, data)

    def delete(self, user_id: UUID) -> MessageSchema:
        return self.crud_service.soft_delete(user_id)

    def _validate_user_creation(self, email: Optional[EmailStr]):
        ensure_or_400(email, "Email is required")
        if email:
            exists_email = self.session.scalar(
                select(User.id).where(
                    User.email == email,
                )
            )
            ensure_or_400(exists_email, "Email already registered")
