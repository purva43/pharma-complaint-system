"""
CAPA Task model for individual tasks within a CAPA.
"""

from sqlalchemy import Column, String, Text, DateTime, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.database import Base


class TaskStatus(str, enum.Enum):
    """Task status workflow."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class CAPATask(Base):
    """CAPA Task model for individual tasks."""
    
    __tablename__ = "capa_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    capa_id = Column(UUID(as_uuid=True), ForeignKey("capas.id"), nullable=False, index=True)
    task_description = Column(Text, nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    due_date = Column(Date, nullable=False, index=True)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING, index=True)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    capa = relationship("CAPA", back_populates="tasks")
    
    def __repr__(self):
        return f"<CAPATask(id={self.id}, capa_id={self.capa_id}, status={self.status})>"
