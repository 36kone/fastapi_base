from sqlalchemy.orm import Session

from services.crud_service import CrudService
from models.users.users import User
from schemas.users.user_schema import UserSchema

crud_service = CrudService(
    session=Session,
    model_class=User,
)


def create_user(user: UserSchema) -> User:
    return crud_service.create(user)