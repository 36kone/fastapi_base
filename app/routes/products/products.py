from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.authentication import get_auth_user
from app.models.users.users import User
from app.schemas import ProductResponse, CreateProduct, UpdateProduct, MessageSchema
from app.services.products.product_service import ProductService

product_router = APIRouter()


@product_router.post("/", status_code=201, response_model=ProductResponse)
def create_product(
    data: CreateProduct,
    service: ProductService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.create(data)


@product_router.get("/", status_code=200, response_model=list[ProductResponse])
def read_products(
    service: ProductService = Depends(), current_user: User = Depends(get_auth_user)
):
    return service.read()


@product_router.get("/{product_id}", status_code=200, response_model=ProductResponse)
def get_product_by_id(
    product_id: UUID,
    service: ProductService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.get_by_id(product_id)


@product_router.put("/{product_id}", status_code=200, response_model=ProductResponse)
def update_product(
    data: UpdateProduct,
    service: ProductService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.update(data)


@product_router.delete("/{product_id}", status_code=200, response_model=MessageSchema)
def delete_product(
    product_id: UUID,
    service: ProductService = Depends(),
    current_user: User = Depends(get_auth_user),
):
    return service.delete(product_id)
