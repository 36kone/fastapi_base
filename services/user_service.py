from sqlalchemy.orm import Session

from models.users.users import User
from schemas.users.user_schema import CreateUser, UserSchema, UpdateUser
from services.crud_service import CrudService


def create_user(user: CreateUser, session: Session) -> User:
    crud_service = CrudService(model_class=User, session=session)
    return crud_service.create(user)


def read_users(session: Session):
    crud_service = CrudService(model_class=User, session=session)
    return crud_service.read()


def get_user_by_id(user_id: int, session: Session) -> User:
    crud_service = CrudService(model_class=User, session=session)
    return crud_service.get_by_id(user_id)


def update_user(data: UpdateUser, session: Session) -> User:
    crud_service = CrudService(model_class=User, session=session)
    return crud_service.update(data.id, data)


def delete_user(user_id: int, session: Session):
    crud_service = CrudService(model_class=User, session=session)
    return crud_service.delete(user_id)
