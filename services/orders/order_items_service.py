from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models import OrderItem
from schemas import CreateOrderItem, UpdateOrderItem
from services.crud_service import CrudService


class OrderItemService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.crud_service = CrudService(OrderItem, session)

    def create(self, order_items: CreateOrderItem) -> OrderItem:
        return self.crud_service.create(order_items)

    def read(self):
        return self.crud_service.read()

    def get_by_id(self, id_: UUID) -> OrderItem:
        return self.crud_service.get_by_id(id_)

    def update(self, order_item: UpdateOrderItem) -> OrderItem:
        return self.crud_service.update(order_item.id, order_item)

    def delete(self, id_: UUID) -> OrderItem:
        return self.crud_service.soft_delete(id_)
