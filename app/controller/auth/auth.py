from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models.users.users import User
from app.schemas.auth.auth_schema import Token
from app.schemas.users.user_schema import UserResponse
from app.services.auth.auth_service import AuthService

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
def read_current_user(auth: User = Depends(get_auth_user)):
    return auth
