from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.exception_utils import ensure_400, ensure_or_404
from app.models import Order
from app.models.users.users import User
from app.schemas.orders.orders_schema import CreateOrder, UpdateOrder
from app.services.crud_service import CrudService
from app.services.orders.order_items_service import OrderItemService
from app.services.products.product_service import ProductService


class OrderService:
    def __init__(self, session: Session):
        self.session = session
        self.crud_service = CrudService(Order, self.session)
        self.order_item_service = OrderItemService(self.session)
        self.product_service = ProductService(self.session)

    def create(self, order: CreateOrder, user: User) -> Order:
        data_dict = order.model_dump(exclude_unset=True, exclude={"order_items"})
        entity = Order(**data_dict)

        entity.user_id = user.id
        entity.amount = 0
        self.session.add(entity)
        self.session.flush()

        amount = 0
        for items in order.order_items:
            product = self.product_service.get_by_id(items.product_id)
            ensure_400(product.quantity == 0, "Insufficient product stock")
            product.quantity -= items.quantity
            items.order_id = entity.id
            self.order_item_service.create(items)
            amount += product.price * items.quantity

        entity.amount = amount
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def read(self):
        return self.crud_service.read()

    def get_by_id(self, id_: UUID) -> Order:
        return self.crud_service.get_by_id(id_)

    def get_by_user_id(self, user_id: UUID):
        return ensure_or_404(
            self.session.scalars(select(Order).where(Order.user_id == user_id)).all(),
            "User orders not found",
        )

    def update(self, id_: UUID, order: UpdateOrder) -> Order:
        return self.crud_service.update(id_, order)

    def delete(self, id_: UUID) -> Order:
        return self.crud_service.soft_delete(id_)
