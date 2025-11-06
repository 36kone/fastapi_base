from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Product
from app.schemas.products.products_schema import CreateProduct, UpdateProduct
from app.services.crud_service import CrudService


class ProductService:
    def __init__(self, session: Session):
        self.session = session
        self.crud_service = CrudService(Product, self.session)

    def create(self, product: CreateProduct) -> Product:
        return self.crud_service.create(product)

    def read(self):
        return self.crud_service.read()

    def get_by_id(self, id_: UUID) -> Product:
        return self.crud_service.get_by_id(id_)

    def update(self, product: UpdateProduct) -> Product:
        return self.crud_service.update(product.id, product)

    def delete(self, id_: UUID) -> Product:
        return self.crud_service.soft_delete(id_)
