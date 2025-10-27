from fastapi import APIRouter

from controllers.auth.auth import auth_router
from controllers.user.user import user_router
from controllers.products.products import product_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(product_router, prefix="/products", tags=["Products"])

api_router.include_router(user_router, prefix="/users", tags=["Users"])
