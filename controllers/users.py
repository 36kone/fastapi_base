from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.users.user_schema import UserResponse, CreateUser, UserSchema, UpdateUser
from services import user_service

users_router = APIRouter()


@users_router.post("/", status_code=201, response_model=UserResponse)
def create_user(data: CreateUser, session: Session = Depends(get_db)):
    return user_service.create_user(data, session)


@users_router.get("/", status_code=200, response_model=list[UserResponse])
def read_users(session: Session = Depends(get_db)):
    return user_service.read_users(session)


@users_router.get("/{user_id}", status_code=200, response_model=UserResponse)
def get_user_by_id(user_id: int, session: Session = Depends(get_db)):
    return user_service.get_user_by_id(user_id, session)


@users_router.put("/{user_id}", status_code=200, response_model=UserResponse)
def update_user(data: UpdateUser, session: Session = Depends(get_db)):
    return user_service.update_user(data, session)


@users_router.delete("/{user_id}", status_code=200)
def delete_user(user_id: int, session: Session = Depends(get_db)):
    return user_service.delete_user(user_id, session)
