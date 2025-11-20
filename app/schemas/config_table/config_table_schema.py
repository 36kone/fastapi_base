from typing import Optional
from uuid import UUID

from pydantic import ConfigDict

from app.schemas import BaseSchema, TimestampedResponse


class ConfigTableSchema(BaseSchema):
    id: UUID
    key: str
    value: str


class CreateConfigTable(BaseSchema):
    key: str
    value: str


class UpdateConfigTable(BaseSchema):
    id: UUID
    key: Optional[str] = None
    value: Optional[str] = None


class ConfigTableResponse(ConfigTableSchema, TimestampedResponse):
    model_config = ConfigDict(from_attributes=True)


class ConfigTableValueResponse(BaseSchema):
    value: str
    model_config = ConfigDict(from_attributes=True)


class ConfigTableGetValuesRequest(BaseSchema):
    keyword: str


class ConfigTableSearchRequest(BaseSchema):
    keyword: Optional[str] = None
    size: int = 10
    page: int = 1
