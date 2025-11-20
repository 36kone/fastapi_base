from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict

from app.schemas.base import BaseSchema


class ProductSchema(BaseSchema):
    id: UUID
    code: str
    name: str
    unit: str
    price: float
    description: str
    quantity: int


class CreateProduct(BaseSchema):
    code: str
    name: str
    unit: str
    price: float
    description: str
    quantity: int


class UpdateProduct(BaseSchema):
    id: UUID
    code: Optional[str] = None
    name: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    quantity: Optional[int] = None


class ProductResponse(ProductSchema):
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProductSearchRequest(BaseSchema):
    keyword: Optional[str] = None
    size: int = 10
    page: int = 1
