"""
Complaint model - core table for customer complaints.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, Date, Enum as SQLEnum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.database import Base


class ComplaintStatus(str, enum.Enum):
    """Complaint status workflow."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_INVESTIGATION = "under_investigation"
   _PENDING_CAPA = "pending_capa"
    CLOSED = "closed"


class ComplaintPriority(str, enum.Enum):
    """Complaint priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(str, enum.Enum):
    """Risk assessment levels."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class Complaint(Base):
    """Core complaint model storing all complaint information."""
    
    __tablename__ = "complaints"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_no = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), index=True)
    
    # Status and priority
    status = Column(SQLEnum(ComplaintStatus), nullable=False, default=ComplaintStatus.DRAFT, index=True)
    priority = Column(SQLEnum(ComplaintPriority), nullable=False, default=ComplaintPriority.MEDIUM, index=True)
    risk_level = Column(SQLEnum(RiskLevel), index=True)
    category = Column(String(100), index=True)
    
    # Complaint details
    description = Column(Text, nullable=False)
    reporter_name = Column(String(255))
    reporter_email = Column(String(255))
    reporter_phone = Column(String(50))
    batch_lot_no = Column(String(100))
    received_date = Column(Date, nullable=False, index=True)
    
    # AI-generated and investigation fields
    summary = Column(Text)
    investigation = Column(Text)
    conclusion = Column(Text)
    
    # Regulatory reporting
    is_reportable = Column(Boolean)
    reporting_deadline = Column(Date)
    
    # Audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    deleted_at = Column(DateTime(timezone=True), index=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="complaints")
    product = relationship("Product", backref="complaints")
    attachments = relationship("Attachment", back_populates="complaint", cascade="all, delete-orphan")
    risk_assessment = relationship("RiskAssessment", back_populates="complaint", uselist=False)
    ai_logs = relationship("AILog", back_populates="complaint", cascade="all, delete-orphan")
    history = relationship("ComplaintHistory", back_populates="complaint", cascade="all, delete-orphan")
    capas = relationship("CAPA", back_populates="complaint", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_status_created_at', 'status', 'created_at'),
        Index('idx_product_received_date', 'product_id', 'received_date'),
    )
    
    def __repr__(self):
        return f"<Complaint(id={self.id}, no={self.complaint_no}, status={self.status})>"
