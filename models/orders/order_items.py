import uuid
from sqlalchemy import Column, String, Float, TIMESTAMP, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # category_id = Column(
    #    UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=False
    # )
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    quantity = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")