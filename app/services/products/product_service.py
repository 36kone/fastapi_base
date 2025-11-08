from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import CreateProduct, UpdateProduct
from app.services.crud_service import CrudService


class ProductService(CrudService):
    def __init__(self, session: Session):
        self.session = session
        super().__init__(Product, self.session)

    def create(self, product: CreateProduct) -> Product:
        return self.create_entity(product)

    def read(self):
        return self.read_entities()

    def get_by_id(self, id_: UUID) -> Product:
        return self.get_entity_by_id(id_)

    def update(self, product: UpdateProduct) -> Product:
        return self.update_entity(product.id, product)

    def delete(self, id_: UUID) -> Product:
        return self.soft_delete_entity(id_)
