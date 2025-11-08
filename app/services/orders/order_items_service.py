from uuid import UUID

from sqlalchemy.orm import Session

from app.models import OrderItem
from app.schemas import CreateOrderItem, UpdateOrderItem
from app.services.crud_service import CrudService


class OrderItemService(CrudService):
    def __init__(self, session: Session):
        self.session = session
        super().__init__(CreateOrderItem, self.session)

    async def create(self, order_items: CreateOrderItem) -> OrderItem:
        return self.create_entity(order_items)

    async def read(self):
        return self.read_entities()

    async def get_by_id(self, id_: UUID) -> OrderItem:
        return self.get_entity_by_id(id_)

    async def update(self, id_: UUID, order_item: UpdateOrderItem) -> OrderItem:
        return self.update_entity(id_, order_item)

    async def delete(self, id_: UUID) -> OrderItem:
        return self.soft_delete_entity(id_)
