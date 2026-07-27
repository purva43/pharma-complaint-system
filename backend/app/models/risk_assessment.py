"""
Risk Assessment model for detailed risk analysis.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.database import Base


class RiskLevel(str, enum.Enum):
    """Risk levels for assessment."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class RiskAssessment(Base):
    """Risk assessment model for detailed risk analysis."""
    
    __tablename__ = "risk_assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), unique=True, nullable=False, index=True)
    risk_level = Column(String(20), nullable=False, index=True)
    severity = Column(Integer)  # 1-10 scale
    probability = Column(Integer)  # 1-10 scale
    impact = Column(Integer)  # 1-10 scale
    risk_score = Column(Integer)  # severity × probability
    justification = Column(Text)
    assessed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    assessed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    complaint = relationship("Complaint", back_populates="risk_assessment")
    
    def __repr__(self):
        return f"<RiskAssessment(id={self.id}, complaint_id={self.complaint_id}, level={self.risk_level})>"
