from fastapi import APIRouter

from app.controller.auth.auth_controller import auth_router
from app.controller.user.user_controller import user_router
from app.controller.products.products_controller import product_router
from app.controller.orders.orders_controller import orders_router
from app.controller.orders.order_items_controller import order_item_router
from app.controller.upload.upload_controller import upload_router
from app.controller.config_table.config_table_service import config_table_router
from app.controller.enum_types.enum_types_controller import enum_types_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(
    config_table_router, prefix="/config-table", tags=["Config Table"]
)
api_router.include_router(enum_types_router, prefix="/enum-types", tags=["Enum Types"])
api_router.include_router(product_router, prefix="/products", tags=["Products"])

api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
api_router.include_router(
    order_item_router, prefix="/order-items", tags=["Order Items"]
)
api_router.include_router(upload_router, prefix="/upload", tags=["Upload"])
