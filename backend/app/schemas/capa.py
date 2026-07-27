"""
Pydantic schemas for CAPA model validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from app.models.capa import CAPAType, CAPAStatus


class CAPABase(BaseModel):
    """Base CAPA schema."""
    complaint_id: Optional[UUID] = None
    type: CAPAType
    description: str = Field(..., min_length=1)
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    due_date: date
    status: CAPAStatus = CAPAStatus.OPEN
    effectiveness: Optional[str] = None


class CAPACreate(CAPABase):
    """Schema for creating a new CAPA."""
    assigned_to: UUID


class CAPAUpdate(BaseModel):
    """Schema for updating a CAPA."""
    type: Optional[CAPAType] = None
    description: Optional[str] = Field(None, min_length=1)
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    assigned_to: Optional[UUID] = None
    due_date: Optional[date] = None
    status: Optional[CAPAStatus] = None
    effectiveness: Optional[str] = None


class CAPAResponse(CAPABase):
    """Schema for CAPA response."""
    id: UUID
    capa_no: str
    assigned_to: UUID
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None
    created_at: datetime
    created_by: Optional[UUID] = None
    
    class Config:
        from_attributes = True


class CAPATaskBase(BaseModel):
    """Base CAPA task schema."""
    task_description: str = Field(..., min_length=1)
    due_date: date
    status: str = "pending"


class CAPATaskCreate(CAPATaskBase):
    """Schema for creating a new CAPA task."""
    capa_id: UUID
    assigned_to: UUID


class CAPATaskUpdate(BaseModel):
    """Schema for updating a CAPA task."""
    task_description: Optional[str] = Field(None, min_length=1)
    assigned_to: Optional[UUID] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class CAPATaskResponse(CAPATaskBase):
    """Schema for CAPA task response."""
    id: UUID
    capa_id: UUID
    assigned_to: UUID
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
