from datetime import datetime, UTC
from typing import Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel

from app.dependencies.exception_utils import ensure_or_404, ensure_400

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CrudService:
    def __init__(self, model_class: Type[ModelType], session: Session):
        self.model_class = model_class
        self.session = session

    def create_entity(self, schema: SchemaType) -> ModelType:
        entity = self.model_class(**schema.model_dump(exclude_unset=True))
        self.session.add(entity)
        self.session.commit()
        return self.get_entity_by_id(entity.id)

    def read_entities(self):
        return self.session.scalars(
            select(self.model_class)
            .where(self.model_class.deleted_at.is_(None))
            .limit(100)
        ).all()

    def get_entity_by_id(self, id_: UUID) -> ModelType | None:
        return ensure_or_404(
            self.session.scalar(
                select(self.model_class).where(
                    self.model_class.id == id_,
                    self.model_class.deleted_at.is_(None),
                )
            ),
            "Entity not found",
        )

    def update_entity(self, id_: UUID, data: SchemaType) -> ModelType:
        entity = self.get_entity_by_id(id_)
        try:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(entity, key, value)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            ensure_400(True, f"Entity update failed: {e}")
            raise e

    def hard_delete_entity(self, id_: UUID):
        entity = self.get_entity_by_id(id_)
        self.session.delete(entity)
        self.session.commit()
        return {"message": "Entity deleted"}

    def soft_delete_entity(self, id_: UUID):
        entity = self.get_entity_by_id(id_)
        ensure_400(entity.deleted_at is not None, "Entity already deleted")
        entity.deleted_at = datetime.now(UTC)
        self.session.add(entity)
        self.session.commit()
        return {"message": "Entity deleted"}
