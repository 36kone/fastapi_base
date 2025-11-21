from uuid import UUID

from sqlalchemy.orm import Session

from sqlalchemy import or_, select, func

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

    async def search(self, keyword: str | None, size: int, page: int):
        offset = (page - 1) * size
        query = select(Product).where(Product.deleted_at.is_(None))

        if keyword:
            pattern = f"%{keyword}%"
            query = query.where(
                or_(
                    Product.name.ilike(pattern),
                    Product.code.ilike(pattern),
                    Product.price.ilike(pattern),
                )
            )

        count_stmt = (
            select(func.count(Product.id))
            .select_from(Product)
            .where(Product.deleted_at.is_(None))
        )

        if keyword:
            pattern = f"%{keyword}%"
            count_stmt = count_stmt.where(
                or_(
                    Product.name.ilike(pattern),
                    Product.code.ilike(pattern),
                    Product.price.ilike(pattern),
                )
            )

        total: int = self.session.scalar(count_stmt)
        stmt = query.limit(size).offset(offset)
        items = self.session.scalars(stmt).all()
        return items, total

    def update(self, product: UpdateProduct) -> Product:
        return self.update_entity(product.id, product)

    def delete(self, id_: UUID) -> Product:
        return self.soft_delete_entity(id_)
