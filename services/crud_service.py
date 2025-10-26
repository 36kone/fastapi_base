from typing import Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel

from dependencies.exception_utils import ensure_or_404

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CrudService:
    def __init__(self, model_class: Type[ModelType], session: Session):
        self.model_class = model_class
        self.session = session

    def create(self, schema: SchemaType) -> ModelType:
        data_dict = schema.model_dump(exclude_unset=True)
        entity = self.model_class(**data_dict)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def read(self):
        return self.session.scalars(select(self.model_class)).all()

    def get_by_id(self, id_: UUID) -> ModelType | None:
        return ensure_or_404(
            self.session.scalar(
                select(self.model_class).where(self.model_class.id == id_)
            ),
            f"{self.model_class} not found",
        )

    def update(self, id_: UUID, data: SchemaType) -> ModelType:
        entity = self.get_by_id(id_)
        try:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(entity, key, value)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id_: UUID):
        entity = self.get_by_id(id_)
        self.session.delete(entity)
        self.session.commit()
        return {"message": f"{self.model_class} deleted"}
