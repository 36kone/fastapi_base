import uuid

from sqlalchemy import Column, String, UUID, Boolean, DateTime, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    password_recovery = Column(String, nullable=True)
    password_recovery_expire = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)

    order = relationship("Order", back_populates="user", lazy="selectin")
