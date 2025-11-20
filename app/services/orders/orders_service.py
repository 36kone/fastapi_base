from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.exception_utils import ensure_400, ensure_or_404
from app.models import Order
from app.models import User
from app.schemas import CreateOrder, UpdateOrder
from app.services.crud_service import CrudService
from app.services.orders.order_items_service import OrderItemService
from app.services.products.product_service import ProductService


class OrderService(CrudService):
    def __init__(self, session: Session):
        self.session = session
        super().__init__(Order, self.session)
        self.order_item_service = OrderItemService(self.session)
        self.product_service = ProductService(self.session)

    async def create(self, order: CreateOrder, user: User) -> Order:
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
            await self.order_item_service.create(items)
            amount += product.price * items.quantity

        entity.amount = amount
        self.session.commit()
        self.session.refresh(entity)
        return entity

    async def read(self):
        return self.read_entities()

    async def get_by_id(self, id_: UUID) -> Order:
        return self.get_entity_by_id(id_)

    async def get_by_user_id(self, user_id: UUID):
        return ensure_or_404(
            self.session.scalars(select(Order).where(Order.user_id == user_id)).all(),
            "User orders not found",
        )

    async def update(self, id_: UUID, order: UpdateOrder) -> Order:
        return self.update_entity(id_, order)

    async def delete(self, id_: UUID) -> Order:
        return self.soft_delete_entity(id_)
