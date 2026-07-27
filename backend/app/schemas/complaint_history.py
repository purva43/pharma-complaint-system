"""
Pydantic schemas for Complaint History model validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ComplaintHistoryBase(BaseModel):
    """Base complaint history schema."""
    action: str = Field(..., max_length=50)
    field_changed: Optional[str] = Field(None, max_length=100)
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason: Optional[str] = None


class ComplaintHistoryCreate(ComplaintHistoryBase):
    """Schema for creating a new history entry."""
    complaint_id: UUID
    changed_by: UUID


class ComplaintHistoryResponse(ComplaintHistoryBase):
    """Schema for complaint history response."""
    id: UUID
    complaint_id: UUID
    changed_by: UUID
    changed_at: datetime
    
    class Config:
        from_attributes = True
