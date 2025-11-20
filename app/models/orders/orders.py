import uuid
from sqlalchemy import Column, String, Float, TIMESTAMP, DateTime, ForeignKey, UUID

# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # category_id = Column(
    #    UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=False
    # )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    order_items = relationship("OrderItem", back_populates="order", lazy="selectin")
    user = relationship("User", back_populates="order", lazy="selectin")
