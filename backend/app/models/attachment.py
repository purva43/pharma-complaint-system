"""
Attachment model for file uploads (PDFs, emails, images).
"""

from sqlalchemy import Column, String, BigInteger, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Attachment(Base):
    """Attachment model for file uploads."""
    
    __tablename__ = "attachments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False, index=True)
    file_size = Column(BigInteger)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    extracted_text = Column(Text)
    is_primary = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    complaint = relationship("Complaint", back_populates="attachments")
    
    # Indexes
    __table_args__ = (
        Index('idx_complaint_primary', 'complaint_id', 'is_primary'),
    )
    
    def __repr__(self):
        return f"<Attachment(id={self.id}, name={self.file_name}, complaint_id={self.complaint_id})>"
