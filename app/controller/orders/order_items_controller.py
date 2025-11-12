from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models import User
from app.schemas import (
    OrderItemResponse,
    CreateOrderItem,
    UpdateOrderItem,
    MessageSchema,
)
from app.services.orders.order_items_service import OrderItemService

order_item_router = APIRouter()


@order_item_router.post("/", status_code=201, response_model=OrderItemResponse)
async def create_order_item(
    data: CreateOrderItem,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderItemService(db)

            return await service.create(data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@order_item_router.get("/", status_code=200, response_model=list[OrderItemResponse])
async def read_order_items(
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderItemService(db)

            return await service.read()
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@order_item_router.get("/{id_}", status_code=200, response_model=OrderItemResponse)
async def get_order_item_by_id(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderItemService(db)

            return await service.get_by_id(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@order_item_router.put("/{id_}", status_code=200, response_model=OrderItemResponse)
async def update_order_item(
    id_: UUID,
    data: UpdateOrderItem,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderItemService(db)

            return await service.update(id_, data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@order_item_router.delete("/{id_}", status_code=200, response_model=MessageSchema)
async def delete_order_item(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderItemService(db)

            return await service.delete(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e
