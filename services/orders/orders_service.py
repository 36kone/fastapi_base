from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models import Order
from schemas import CreateOrder, UpdateOrder
from services.crud_service import CrudService
from services.orders.order_items_service import OrderItemService


class OrderService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.crud_service = CrudService(Order, session)
        self.order_item_service = OrderItemService(self.session)

    def create(self, order: CreateOrder) -> Order:
        data_dict = order.model_dump(exclude_unset=True, exclude={"order_items"})
        entity = Order(**data_dict)

        self.session.add(entity)
        self.session.flush()

        for items in order.order_items:
            items.order_id = entity.id
            self.order_item_service.create(items)

        self.session.commit()
        self.session.refresh(entity)
        return entity

    def read(self):
        return self.crud_service.read()

    def get_by_id(self, id_: UUID) -> Order:
        return self.crud_service.get_by_id(id_)

    def update(self, order: UpdateOrder) -> Order:
        return self.crud_service.update(order.id, order)

    def delete(self, id_: UUID) -> Order:
        return self.crud_service.soft_delete(id_)
