from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict

from app.schemas.base import BaseSchema


class OrderItemSchema(BaseSchema):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: float


class CreateOrderItem(BaseSchema):
    order_id: UUID
    product_id: UUID
    quantity: float


class UpdateOrderItem(BaseSchema):
    id: UUID
    order_id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    quantity: Optional[float] = None


class OrderItemResponse(OrderItemSchema):
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
