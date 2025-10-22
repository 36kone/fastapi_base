from fastapi import APIRouter

from controllers.clients import clients_router
from controllers.auth import login_router
from controllers.orders import orders_router
from controllers.products import products_router

api_router = APIRouter()

api_router.include_router(login_router, prefix="/auth", tags=["Auth"])
api_router.include_router(clients_router, prefix="/clients", tags=["Clients"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
