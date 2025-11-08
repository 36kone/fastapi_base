from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.dependencies.exception_utils import ensure_or_404, ensure_or_400
from app.models import User
from app.schemas import CreateUser, UpdateUser, MessageSchema
from app.services.crud_service import CrudService


class UserService(CrudService):
    def __init__(self, session: Session):
        self.session = session
        super().__init__(User, self.session)

    def create(self, user: CreateUser) -> User:
        self.__validate_user_creation(user)
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
        return self.read_entities()

    def get_by_id(self, user_id: UUID) -> User:
        return self.get_entity_by_id(user_id)

    def get_by_email(self, email: str) -> User:
        return ensure_or_404(
            self.session.scalar((select(User).where(User.email == email))),
            "User not found",
        )

    def update(self, data: UpdateUser) -> User:
        return self.update_entity(data.id, data)

    def delete(self, user_id: UUID) -> MessageSchema:
        return self.soft_delete_entity(user_id)

    def __validate_user_creation(self, user: CreateUser):
        ensure_or_400(user.email, "Email is required")
        ensure_or_400(user.phone, "Phone is required")
        if user.email:
            exists_email = self.session.scalar(
                select(User.id).where(
                    User.email == user.email,
                )
            )
            ensure_or_400(not exists_email, "Email already registered")
        if user.phone:
            exists_phone = self.session.scalar(
                select(User.id).where(
                    User.phone == user.phone,
                )
            )
            ensure_or_400(not exists_phone, "Phone already registered")
