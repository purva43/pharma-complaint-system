"""
AI Log model for tracking AI processing and audit trail.
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class AILog(Base):
    """AI processing log for audit trail and debugging."""
    
    __tablename__ = "ai_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), index=True)
    node_name = Column(String(100), nullable=False, index=True)
    input_data = Column(JSONB)
    output_data = Column(JSONB)
    confidence_score = Column(Numeric(5, 4))  # 0.0000 to 1.0000
    processing_time_ms = Column(Integer)
    model_used = Column(String(100))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    complaint = relationship("Complaint", back_populates="ai_logs")
    
    # Indexes
    __table_args__ = (
        Index('idx_complaint_node', 'complaint_id', 'node_name'),
    )
    
    def __repr__(self):
        return f"<AILog(id={self.id}, node={self.node_name}, complaint_id={self.complaint_id})>"
