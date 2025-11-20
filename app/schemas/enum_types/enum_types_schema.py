from datetime import datetime
from typing import Optional

from pydantic import ConfigDict

from app.schemas.base import BaseSchema
from uuid import UUID


class EnumTypesSchema(BaseSchema):
    type: str
    key: str
    value: str


class EnumTypesResponse(EnumTypesSchema):
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class EnumTypesUpdate(EnumTypesSchema):
    id: UUID
