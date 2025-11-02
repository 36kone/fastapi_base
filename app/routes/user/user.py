from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.authentication import get_auth_user
from app.models.users.users import User
from app.schemas import UserResponse, CreateUser, UpdateUser, MessageSchema
from app.services.user.user_service import UserService

user_router = APIRouter()


@user_router.post("/", status_code=201, response_model=UserResponse)
def create_user(
    data: CreateUser,
    service: UserService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.create(data)


@user_router.get("/", status_code=200, response_model=list[UserResponse])
def read_users(
    service: UserService = Depends(), current_user: User = Depends(get_auth_user)
):
    return service.read()


@user_router.get("/{user_id}", status_code=200, response_model=UserResponse)
def get_user_by_id(
    user_id: UUID,
    service: UserService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.get_by_id(user_id)


@user_router.get("/user/{email}", status_code=200, response_model=UserResponse)
def get_user_by_email(
    email: str,
    service: UserService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.get_by_email(email)


@user_router.put("/{user_id}", status_code=200, response_model=UserResponse)
def update_user(
    data: UpdateUser,
    service: UserService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.update(data)


@user_router.delete("/{user_id}", status_code=200, response_model=MessageSchema)
def delete_user(
    user_id: UUID,
    service: UserService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.delete(user_id)
