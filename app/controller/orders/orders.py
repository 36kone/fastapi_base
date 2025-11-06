from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models.users.users import User
from app.schemas.message_schema import MessageSchema
from app.schemas.orders.orders_schema import OrderResponse, CreateOrder, UpdateOrder
from app.services.orders.orders_service import OrderService

orders_router = APIRouter()


@orders_router.post("/", status_code=201, response_model=OrderResponse)
def create_order(
    data: CreateOrder,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return OrderService(db).create(data, current_user)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.get("/", status_code=200, response_model=list[OrderResponse])
def read_orders(current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            return OrderService(db).read()
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.get("/{id_}", status_code=200, response_model=OrderResponse)
def get_order_by_id(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return OrderService(db).get_by_id(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.get(
    "/user/{user_id}", status_code=200, response_model=list[OrderResponse]
)
def get_orders_by_user_id(
    user_id: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return OrderService(db).get_by_user_id(user_id)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.put("/{id_}", status_code=200, response_model=OrderResponse)
def update_order(
    id_: UUID,
    data: UpdateOrder,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return OrderService(db).update(id_, data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@orders_router.delete("/{id_}", status_code=200, response_model=MessageSchema)
def delete_order(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return OrderService(db).delete(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e
