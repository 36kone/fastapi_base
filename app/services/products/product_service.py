from uuid import UUID

from sqlalchemy.orm import Session

from sqlalchemy import or_

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

    async def search(self, keyword: str, size: int, page: int):
        query = self.session.query(Product).filter(Product.deleted_at.is_(None))

        if keyword:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{keyword}%"),
                    Product.code.ilike(f"%{keyword}%"),
                    Product.price.ilike(f"%{keyword}%"),
                )
            )

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def update(self, product: UpdateProduct) -> Product:
        return self.update_entity(product.id, product)

    def delete(self, id_: UUID) -> Product:
        return self.soft_delete_entity(id_)
