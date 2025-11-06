from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderSchema(BaseModel):
    id: UUID
    user_id: UUID
    description: Optional[str] = None
    amount: float


class CreateOrderItem(BaseModel):
    order_id: Optional[UUID] = None
    product_id: UUID
    quantity: int


class CreateOrder(BaseModel):
    description: str
    order_items: List[CreateOrderItem]


class UpdateOrder(BaseModel):
    id: UUID
    description: Optional[str] = None
    amount: Optional[float] = None


class OrderItem(BaseModel):
    id: UUID
    product_id: UUID
    quantity: float


class OrderResponse(OrderSchema):
    order_items: List[OrderItem] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
