"""
Product model for complaint association.
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Product(Base):
    """Product model for complaint association."""
    
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String(255), nullable=False, index=True)
    product_code = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), index=True)
    description = Column(String(500))
    manufacturer = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.product_name}, code={self.product_code})>"
