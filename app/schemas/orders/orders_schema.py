from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import ConfigDict, EmailStr

from app.schemas.base import BaseSchema


class OrderSchema(BaseSchema):
    id: UUID
    user_id: UUID
    description: Optional[str] = None
    amount: float


class CreateOrderItem(BaseSchema):
    order_id: Optional[UUID] = None
    product_id: UUID
    quantity: int


class CreateOrder(BaseSchema):
    description: str
    order_items: List[CreateOrderItem]


class UpdateOrder(BaseSchema):
    id: UUID
    description: Optional[str] = None
    amount: Optional[float] = None


class OrderItem(BaseSchema):
    id: UUID
    product_id: UUID
    quantity: float


class User(BaseSchema):
    id: UUID
    name: str
    phone: str
    email: EmailStr


class OrderResponse(OrderSchema):
    order_items: List[OrderItem] = []
    user: User
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OrderSearchRequest(BaseSchema):
    keyword: Optional[str] = None
    user_id: Optional[UUID] = None
    amount: Optional[float] = None
    size: int = 10
    page: int = 1
