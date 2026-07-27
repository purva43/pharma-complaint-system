"""
Pydantic schemas for Complaint model validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from app.models.complaint import ComplaintStatus, ComplaintPriority, RiskLevel


class ComplaintBase(BaseModel):
    """Base complaint schema."""
    product_id: Optional[UUID] = None
    status: ComplaintStatus = ComplaintStatus.DRAFT
    priority: ComplaintPriority = ComplaintPriority.MEDIUM
    risk_level: Optional[RiskLevel] = None
    category: Optional[str] = Field(None, max_length=100)
    description: str = Field(..., min_length=1)
    reporter_name: Optional[str] = Field(None, max_length=255)
    reporter_email: Optional[str] = Field(None, max_length=255)
    reporter_phone: Optional[str] = Field(None, max_length=50)
    batch_lot_no: Optional[str] = Field(None, max_length=100)
    received_date: date
    summary: Optional[str] = None
    investigation: Optional[str] = None
    conclusion: Optional[str] = None
    is_reportable: Optional[bool] = None
    reporting_deadline: Optional[date] = None


class ComplaintCreate(ComplaintBase):
    """Schema for creating a new complaint."""
    pass


class ComplaintUpdate(BaseModel):
    """Schema for updating a complaint."""
    product_id: Optional[UUID] = None
    status: Optional[ComplaintStatus] = None
    priority: Optional[ComplaintPriority] = None
    risk_level: Optional[RiskLevel] = None
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    reporter_name: Optional[str] = Field(None, max_length=255)
    reporter_email: Optional[str] = Field(None, max_length=255)
    reporter_phone: Optional[str] = Field(None, max_length=50)
    batch_lot_no: Optional[str] = Field(None, max_length=100)
    received_date: Optional[date] = None
    summary: Optional[str] = None
    investigation: Optional[str] = None
    conclusion: Optional[str] = None
    is_reportable: Optional[bool] = None
    reporting_deadline: Optional[date] = None


class ComplaintResponse(ComplaintBase):
    """Schema for complaint response."""
    id: UUID
    complaint_no: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ComplaintListResponse(BaseModel):
    """Schema for paginated complaint list."""
    items: list[ComplaintResponse]
    total: int
    page: int
    page_size: int
