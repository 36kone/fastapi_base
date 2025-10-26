from fastapi import APIRouter

from schemas.users.user_schema import UserSchema, UserResponse
from services import user_service

users_router = APIRouter()


@users_router.post("/", status_code=201, response_model=UserResponse)
def create_user(data: UserSchema):
    return user_service.create_user(data)
