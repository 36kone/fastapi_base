import uuid
from sqlalchemy import Column, String, TIMESTAMP, func, DateTime, UUID

# from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class EnumTypes(Base):
    __tablename__ = "enum_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
