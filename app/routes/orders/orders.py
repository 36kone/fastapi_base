from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.authentication import get_auth_user
from app.models.users.users import User
from app.schemas import OrderResponse, CreateOrder, UpdateOrder, MessageSchema
from app.services.orders.orders_service import OrderService

orders_router = APIRouter()


@orders_router.post("/", status_code=201, response_model=OrderResponse)
def create_order(
    data: CreateOrder,
    service: OrderService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.create(data, current_user)


@orders_router.get("/", status_code=200, response_model=list[OrderResponse])
def read_orders(
    service: OrderService = Depends(), current_user: User = Depends(get_auth_user)
):
    return service.read()


@orders_router.get("/{order_id}", status_code=200, response_model=OrderResponse)
def get_order_by_id(
    order_id: UUID,
    service: OrderService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.get_by_id(order_id)


@orders_router.get("/user/{user_id}", status_code=200, response_model=list[OrderResponse])
def get_orders_by_user_id(
    user_id: UUID,
    service: OrderService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.get_by_user_id(user_id)


@orders_router.put("/{order_id}", status_code=200, response_model=OrderResponse)
def update_order(
    data: UpdateOrder,
    service: OrderService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.update(data)


@orders_router.delete("/{order_id}", status_code=200, response_model=MessageSchema)
def delete_order(
    user_id: UUID,
    service: OrderService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.delete(user_id)
