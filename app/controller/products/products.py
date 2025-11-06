from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models.users.users import User
from app.schemas.message_schema import MessageSchema
from app.schemas.products.products_schema import (
    CreateProduct,
    ProductResponse,
    UpdateProduct,
)
from app.services.products.product_service import ProductService

product_router = APIRouter()


@product_router.post("/", status_code=201, response_model=ProductResponse)
def create_product(
    data: CreateProduct,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return ProductService(db).create(data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@product_router.get("/", status_code=200, response_model=list[ProductResponse])
def read_products(
    current_user: User = Depends(get_auth_user)
):
    try:
        with get_db() as db:
            return ProductService(db).read()
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@product_router.get("/{id_}", status_code=200, response_model=ProductResponse)
def get_product_by_id(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return ProductService(db).get_by_id(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@product_router.put("/{id_}", status_code=200, response_model=ProductResponse)
def update_product(
    data: UpdateProduct,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return ProductService(db).update(data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@product_router.delete("/{id_}", status_code=200, response_model=MessageSchema)
def delete_product(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            return ProductService(db).delete(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e
