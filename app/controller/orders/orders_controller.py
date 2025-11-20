from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models import User
from app.schemas import (
    OrderResponse,
    CreateOrder,
    UpdateOrder,
    MessageSchema,
    PaginatedResponse,
    OrderSearchRequest,
)
from app.services.orders.orders_service import OrderService

orders_router = APIRouter()


@orders_router.post("/", status_code=201, response_model=OrderResponse)
async def create_order(
    data: CreateOrder,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderService(db)

            return await service.create(data, current_user)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.get("/", status_code=200, response_model=list[OrderResponse])
async def read_orders(current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            service = OrderService(db)

            return await service.read()
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.get("/{id_}", status_code=200, response_model=OrderResponse)
async def get_order_by_id(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderService(db)

            return await service.get_by_id(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.get(
    "/user/{user_id}", status_code=200, response_model=list[OrderResponse]
)
async def get_orders_by_user_id(
    user_id: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderService(db)

            return await service.get_by_user_id(user_id)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.post(
    "/search", status_code=200, response_model=PaginatedResponse[OrderResponse]
)
async def search_orders(
    search_request: OrderSearchRequest,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderService(db)

            items, total = await service.search(filters=search_request)

            return PaginatedResponse.create(
                total=total,
                page=search_request.page,
                size=search_request.size,
                items=[
                    OrderResponse.model_validate(i, from_attributes=True) for i in items
                ],
            )
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.put("/{id_}", status_code=200, response_model=OrderResponse)
async def update_order(
    id_: UUID,
    data: UpdateOrder,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderService(db)

            return await service.update(id_, data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.delete("/{id_}", status_code=200, response_model=MessageSchema)
async def delete_order(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = OrderService(db)

            return await service.delete(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e
