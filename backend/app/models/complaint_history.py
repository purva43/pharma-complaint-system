"""
Complaint History model for audit trail.
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class ComplaintHistory(Base):
    """Audit trail model for complaint changes."""
    
    __tablename__ = "complaint_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    field_changed = Column(String(100))
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    reason = Column(Text)
    
    # Relationships
    complaint = relationship("Complaint", back_populates="history")
    
    # Indexes
    __table_args__ = (
        Index('idx_complaint_changed_at', 'complaint_id', 'changed_at'),
    )
    
    def __repr__(self):
        return f"<ComplaintHistory(id={self.id}, action={self.action}, complaint_id={self.complaint_id})>"
