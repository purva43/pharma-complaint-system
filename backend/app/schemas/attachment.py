"""
Pydantic schemas for Attachment model validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class AttachmentBase(BaseModel):
    """Base attachment schema."""
    file_name: str = Field(..., max_length=255)
    file_path: str = Field(..., max_length=500)
    file_type: str = Field(..., max_length=100)
    file_size: Optional[int] = None
    is_primary: bool = False


class AttachmentCreate(AttachmentBase):
    """Schema for creating a new attachment."""
    complaint_id: UUID


class AttachmentResponse(AttachmentBase):
    """Schema for attachment response."""
    id: UUID
    complaint_id: UUID
    uploaded_at: datetime
    uploaded_by: Optional[UUID] = None
    extracted_text: Optional[str] = None
    
    class Config:
        from_attributes = True
