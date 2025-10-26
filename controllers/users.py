from fastapi import APIRouter, Depends

from schemas import UserResponse, CreateUser, UpdateUser, MessageSchema
from services.user_service import UserService

users_router = APIRouter()


@users_router.post("/", status_code=201, response_model=UserResponse)
def create_user(data: CreateUser, service: UserService = Depends()):
    return service.create(data)


@users_router.get("/", status_code=200, response_model=list[UserResponse])
def read_users(service: UserService = Depends()):
    return service.read()


@users_router.get("/{user_id}", status_code=200, response_model=UserResponse)
def get_user_by_id(user_id: int, service: UserService = Depends()):
    return service.get_by_id(user_id)


@users_router.get("/user/{email}", status_code=200, response_model=UserResponse)
def get_user_by_email(email: str, service: UserService = Depends()):
    return service.get_by_email(email)


@users_router.put("/{user_id}", status_code=200, response_model=UserResponse)
def update_user(data: UpdateUser, service: UserService = Depends()):
    return service.update(data)


@users_router.delete("/{user_id}", status_code=200, response_model=MessageSchema)
def delete_user(user_id: int, service: UserService = Depends()):
    return service.delete(user_id)
