from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models import Product
from schemas import CreateProduct, UpdateProduct
from services.crud_service import CrudService


class ProductService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.crud_service = CrudService(Product, session)

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
