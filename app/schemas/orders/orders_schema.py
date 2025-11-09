from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

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


class OrderResponse(OrderSchema):
    order_items: List[OrderItem] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
