from typing import Optional
from uuid import UUID

from app.models import ConfigTable
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.schemas import CreateConfigTable, UpdateConfigTable
from app.services.crud_service import CrudService


class ConfigTableService(CrudService):
    def __init__(self, session: Session):
        self.session = session
        super().__init__(ConfigTable, self.session)

    def create(self, data: CreateConfigTable) -> ConfigTable:
        return self.create_entity(data)

    def read(self):
        return self.read_entities()

    def get_by_id(self, id_: UUID) -> ConfigTable:
        return self.get_entity_by_id(id_)

    def get_value(self, key: str):
        return self.session.scalar(
            select(ConfigTable.value).where(ConfigTable.key == key)
        )

    def get_values_by_keyword(self, keyword: str) -> dict[str, str]:
        rows = self.session.execute(
            select(ConfigTable.key, ConfigTable.value).where(
                ConfigTable.key.ilike(f"%{keyword}%")
            )
        ).all()
        return {key: value for key, value in rows}

    async def search(self, keyword: str, size: int, page: int):
        base = select(ConfigTable)
        offset = (page - 1) * size

        if keyword:
            pattern = f"%{keyword}%"
            base = base.where(ConfigTable.key.ilike(pattern))

        count_stmt = select(func.count(ConfigTable.id)).select_from(ConfigTable)

        if keyword:
            pattern = f"%{keyword}%"
            count_stmt = count_stmt.where(ConfigTable.key.ilike(pattern))

        total = self.session.scalar(count_stmt)
        stmt = base.limit(size).offset(offset)
        items = self.session.scalars(stmt).all()
        return items, total

    def update(self, data: UpdateConfigTable) -> Optional[ConfigTable]:
        return self.update_entity(data.id, data)

    def delete(self, id_: UUID):
        return self.soft_delete_entity(id_)
