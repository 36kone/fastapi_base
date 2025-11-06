from uuid import UUID

from sqlalchemy.orm import Session

from app.models import OrderItem
from app.schemas.orders.order_items_schema import CreateOrderItem, UpdateOrderItem
from app.services.crud_service import CrudService


class OrderItemService:
    def __init__(self, session: Session):
        self.session = session
        self.crud_service = CrudService(OrderItem, self.session)

    async def create(self, order_items: CreateOrderItem) -> OrderItem:
        return self.crud_service.create(order_items)

    async def read(self):
        return self.crud_service.read()

    async def get_by_id(self, id_: UUID) -> OrderItem:
        return self.crud_service.get_by_id(id_)

    async def update(self, id_: UUID, order_item: UpdateOrderItem) -> OrderItem:
        return self.crud_service.update(id_, order_item)

    async def delete(self, id_: UUID) -> OrderItem:
        return self.crud_service.soft_delete(id_)
