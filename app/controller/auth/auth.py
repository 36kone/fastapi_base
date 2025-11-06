from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models import User
from app.schemas import Token, UserResponse, ChangePasswordRequest, MessageSchema
from app.services.auth.auth_service import AuthService
from app.services.user.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        with get_db() as db:
            return AuthService(db).login(form_data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@auth_router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            return UserService(db).get_by_id(current_user.id)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@auth_router.post("/change-password", response_model=MessageSchema)
def change_password(
    data: ChangePasswordRequest, current_user: User = Depends(get_auth_user)
):
    try:
        with get_db() as db:
            return AuthService(db).change_password(data, current_user.id)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e
