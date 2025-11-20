from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models import User
from app.schemas import (
    CreateProduct,
    ProductResponse,
    UpdateProduct,
    MessageSchema,
    PaginatedResponse,
    ProductSearchRequest,
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
            service = ProductService(db)

            return service.create(data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@product_router.get("/", status_code=200, response_model=list[ProductResponse])
def read_products(current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            service = ProductService(db)

            return service.read()
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
            service = ProductService(db)

            return service.get_by_id(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@product_router.post(
    "/search", status_code=200, response_model=PaginatedResponse[ProductResponse]
)
async def search_products(
    search_request: ProductSearchRequest,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ProductService(db)

            items, total = await service.search(
                keyword=search_request.keyword,
                size=search_request.size,
                page=search_request.page,
            )

            return PaginatedResponse.create(
                total=total,
                page=search_request.page,
                size=search_request.size,
                items=[
                    ProductResponse.model_validate(i, from_attributes=True)
                    for i in items
                ],
            )
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
            service = ProductService(db)

            return service.update(data)
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
            service = ProductService(db)

            return service.delete(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e
