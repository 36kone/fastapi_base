from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.authentication import get_auth_user
from models.users.users import User
from schemas import Token
from schemas.users.user_schema import UserResponse
from services.auth.auth_service import AuthService

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()
):
    return service.login(form_data)


@auth_router.get("/me", response_model=UserResponse)
def read_current_user(auth: User = Depends(get_auth_user)):
    return auth
