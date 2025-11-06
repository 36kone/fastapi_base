from uuid import UUID

from sqlalchemy.orm import Session

from app.models import OrderItem
from app.schemas.orders.order_items_schema import CreateOrderItem, UpdateOrderItem
from app.services.crud_service import CrudService


class OrderItemService:
    def __init__(self, session: Session):
        self.session = session
        self.crud_service = CrudService(OrderItem, self.session)

    def create(self, order_items: CreateOrderItem) -> OrderItem:
        return self.crud_service.create(order_items)

    def read(self):
        return self.crud_service.read()

    def get_by_id(self, id_: UUID) -> OrderItem:
        return self.crud_service.get_by_id(id_)

    def update(self, id_: UUID, order_item: UpdateOrderItem) -> OrderItem:
        return self.crud_service.update(id_, order_item)

    def delete(self, id_: UUID) -> OrderItem:
        return self.crud_service.soft_delete(id_)
