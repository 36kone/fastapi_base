from fastapi import APIRouter

from controllers.auth.auth import auth_router
from controllers.user.user import user_router
from controllers.products.products import product_router
from controllers.orders.orders import orders_router
from controllers.orders.order_items import order_item_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(product_router, prefix="/products", tags=["Products"])

api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
api_router.include_router(order_item_router, prefix="/order-items", tags=["Order Items"])

