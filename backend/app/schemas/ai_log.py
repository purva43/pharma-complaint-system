"""
Pydantic schemas for AI Log model validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from uuid import UUID


class AILogBase(BaseModel):
    """Base AI log schema."""
    node_name: str = Field(..., max_length=100)
    input_data: Optional[dict[str, Any]] = None
    output_data: Optional[dict[str, Any]] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = Field(None, max_length=100)
    error_message: Optional[str] = None


class AILogCreate(AILogBase):
    """Schema for creating a new AI log."""
    complaint_id: UUID


class AILogResponse(AILogBase):
    """Schema for AI log response."""
    id: UUID
    complaint_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
