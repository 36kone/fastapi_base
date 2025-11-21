from uuid import UUID

from sqlalchemy import select, func
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
            role=user.role if user.role else "user",
            is_active=True,
        )
        self.session.add(entity)
        self.session.commit()
        return self.get_entity_by_id(entity.id)

    def read(self) -> list[User]:
        return self.read_entities()

    def get_by_id(self, user_id: UUID) -> User:
        return self.get_entity_by_id(user_id)

    def get_by_email(self, email: str) -> User:
        return ensure_or_404(
            self.session.scalar((select(User).where(User.email == email))),
            "User not found",
        )

    async def search(self, keyword: str | None, size: int, page: int):
        query = select(User).where(User.deleted_at.is_(None))
        offset = (page - 1) * size

        if keyword:
            query = query.where(User.name.ilike(f"%{keyword}%"))

        count_stmt = (
            select(func.count(User.id))
            .select_from(User)
            .where(User.deleted_at.is_(None))
        )

        if keyword:
            count_stmt = count_stmt.where(User.name.ilike(f"%{keyword}%"))

        total: int = self.session.scalar(count_stmt)
        stmt = query.limit(size).offset(offset)
        items = self.session.scalars(stmt).all()
        return items, total

    def update(self, data: UpdateUser) -> User:
        return self.update_entity(data.id, data)

    def delete(self, user_id: UUID) -> MessageSchema:
        return self.soft_delete_entity(user_id)

    def __validate_user_creation(self, user: CreateUser):
        ensure_or_400(user.email, "Email is required")
        ensure_or_400(user.phone, "Phone is required")

        stmt = select(User.id).where(
            (User.email == user.email) | (User.phone == user.phone)
        )

        exists = self.session.scalar(stmt)
        ensure_or_400(not exists, "Email or phone already registered")
