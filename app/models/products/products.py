import uuid
from sqlalchemy import Column, String, Float, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # category_id = Column(
    #    UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=False
    # )
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    order_items = relationship("OrderItem", back_populates="product")
