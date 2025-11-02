from uuid import UUID

from fastapi import APIRouter, Depends

from dependencies.authentication import get_auth_user
from models.users.users import User
from schemas import OrderItemResponse, CreateOrderItem, UpdateOrderItem, MessageSchema
from services.orders.order_items_service import OrderItemService

order_item_router = APIRouter()


@order_item_router.post("/", status_code=201, response_model=OrderItemResponse)
def create_order_item(
    data: CreateOrderItem,
    service: OrderItemService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.create(data)


@order_item_router.get("/", status_code=200, response_model=list[OrderItemResponse])
def read_order_items(
    service: OrderItemService = Depends(), current_user: User = Depends(get_auth_user)
):
    return service.read()


@order_item_router.get("/{order_item_id}", status_code=200, response_model=OrderItemResponse)
def get_order_item_by_id(
    order_id: UUID,
    service: OrderItemService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.get_by_id(order_id)


@order_item_router.put("/{order_item_id}", status_code=200, response_model=OrderItemResponse)
def update_order_item(
    data: UpdateOrderItem,
    service: OrderItemService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.update(data)


@order_item_router.delete("/{order_item_id}", status_code=200, response_model=MessageSchema)
def delete_order_item(
    user_id: UUID,
    service: OrderItemService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.delete(user_id)
