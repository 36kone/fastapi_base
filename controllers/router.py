from fastapi import APIRouter

from controllers.auth import login_router
from controllers.users import users_router

api_router = APIRouter()

api_router.include_router(login_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
