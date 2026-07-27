"""
CAPA model for Corrective and Preventive Actions.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.database import Base


class CAPAType(str, enum.Enum):
    """CAPA type classification."""
    CORRECTIVE = "corrective"
    PREVENTIVE = "preventive"
    BOTH = "both"


class CAPAStatus(str, enum.Enum):
    """CAPA status workflow."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_VERIFICATION = "pending_verification"
    CLOSED = "closed"


class CAPA(Base):
    """CAPA model for corrective and preventive actions."""
    
    __tablename__ = "capas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"), index=True)
    capa_no = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(SQLEnum(CAPAType), nullable=False)
    description = Column(Text, nullable=False)
    root_cause = Column(Text)
    corrective_action = Column(Text)
    preventive_action = Column(Text)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    due_date = Column(Date, nullable=False, index=True)
    status = Column(SQLEnum(CAPAStatus), nullable=False, default=CAPAStatus.OPEN, index=True)
    effectiveness = Column(Text)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    complaint = relationship("Complaint", back_populates="capas")
    tasks = relationship("CAPATask", back_populates="capa", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CAPA(id={self.id}, no={self.capa_no}, status={self.status})>"
