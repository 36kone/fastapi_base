import uuid
from sqlalchemy import Column, String, UUID, TIMESTAMP, func

# from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class ConfigTable(Base):
    __tablename__ = "config_table"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
