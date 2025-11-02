from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: UUID
    code: str
    name: str
    unit: str
    price: float
    description: str
    quantity: int


class CreateProduct(BaseModel):
    code: str
    name: str
    unit: str
    price: float
    description: str
    quantity: int


class UpdateProduct(BaseModel):
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
