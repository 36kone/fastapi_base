from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.exception_utils import ensure_or_404
from app.models import EnumTypes
from app.schemas import EnumTypesSchema, EnumTypesUpdate
from app.services.crud_service import CrudService


class EnumTypesService(CrudService):
    def __init__(self, session: Session):
        self.session = session
        super().__init__(EnumTypes, self.session)

    def create(self, data: EnumTypesSchema):
        return self.create_entity(data)

    def read(self):
        return self.read_entities()

    def get_by_type(self, type_: str):
        return ensure_or_404(
            self.session.scalars(
                select(EnumTypes).where(
                    EnumTypes.type == type_,
                    EnumTypes.deleted_at.is_(None),
                )
            ).all(),
            "Enum type not found",
        )

    def get_by_id(self, id_: UUID):
        return self.get_entity_by_id(id_)

    def update(self, data: EnumTypesUpdate):
        return self.update_entity(data.id, data)

    def delete(self, id_: UUID):
        return self.soft_delete_entity(id_)
