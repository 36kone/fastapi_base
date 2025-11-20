from datetime import datetime, timezone
from typing import Optional

from zoneinfo import ZoneInfo
from pydantic import BaseModel, field_validator, ConfigDict

SP_TZ = ZoneInfo("America/Sao_Paulo")
UTC = timezone.utc


def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
        ser_json_t = {"by_alias": True}


# CONVERTE O TIMESTAMP DO DB DE UTC PARA FUSO DE SP
class TimestampedResponse(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("created_at", "updated_at", "deleted_at", mode="before")
    @classmethod
    def convert_utc_to_sp(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is None:
            return value

        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)

        return value.astimezone(SP_TZ)
