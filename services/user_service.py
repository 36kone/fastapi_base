from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.exception_utils import ensure_or_404
from models.users.users import User
from schemas import CreateUser, UpdateUser, MessageSchema
from services.crud_service import CrudService


class UserService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.crud_service = CrudService(User, session)

    def create(self, user: CreateUser) -> User:
        return self.crud_service.create(user)

    def read(self) -> list[User]:
        return self.crud_service.read()

    def get_by_id(self, user_id: int) -> User:
        return self.crud_service.get_by_id(user_id)

    def get_by_email(self, email: str) -> User:
        return ensure_or_404(
            self.session.scalar((select(User).where(User.email == email))),
            "User not found",
        )

    def update(self, data: UpdateUser) -> User:
        return self.crud_service.update(data.id, data)

    def delete(self, user_id: int) -> MessageSchema:
        return self.crud_service.delete(user_id)
