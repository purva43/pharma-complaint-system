"""
Pydantic schemas for Risk Assessment model validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class RiskAssessmentBase(BaseModel):
    """Base risk assessment schema."""
    risk_level: str = Field(..., max_length=20)
    severity: Optional[int] = Field(None, ge=1, le=10)
    probability: Optional[int] = Field(None, ge=1, le=10)
    impact: Optional[int] = Field(None, ge=1, le=10)
    risk_score: Optional[int] = None
    justification: Optional[str] = None


class RiskAssessmentCreate(RiskAssessmentBase):
    """Schema for creating a new risk assessment."""
    complaint_id: UUID


class RiskAssessmentUpdate(BaseModel):
    """Schema for updating a risk assessment."""
    risk_level: Optional[str] = Field(None, max_length=20)
    severity: Optional[int] = Field(None, ge=1, le=10)
    probability: Optional[int] = Field(None, ge=1, le=10)
    impact: Optional[int] = Field(None, ge=1, le=10)
    risk_score: Optional[int] = None
    justification: Optional[str] = None


class RiskAssessmentResponse(RiskAssessmentBase):
    """Schema for risk assessment response."""
    id: UUID
    complaint_id: UUID
    assessed_by: UUID
    assessed_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
