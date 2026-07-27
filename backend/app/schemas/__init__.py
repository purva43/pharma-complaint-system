"""
Import all schemas for easy access.
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData,
)
from app.schemas.product import (
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.schemas.complaint import (
    ComplaintBase,
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
    ComplaintListResponse,
)
from app.schemas.attachment import (
    AttachmentBase,
    AttachmentCreate,
    AttachmentResponse,
)
from app.schemas.risk_assessment import (
    RiskAssessmentBase,
    RiskAssessmentCreate,
    RiskAssessmentUpdate,
    RiskAssessmentResponse,
)
from app.schemas.ai_log import (
    AILogBase,
    AILogCreate,
    AILogResponse,
)
from app.schemas.complaint_history import (
    ComplaintHistoryBase,
    ComplaintHistoryCreate,
    ComplaintHistoryResponse,
)
from app.schemas.capa import (
    CAPABase,
    CAPACreate,
    CAPAUpdate,
    CAPAResponse,
    CAPATaskBase,
    CAPATaskCreate,
    CAPATaskUpdate,
    CAPATaskResponse,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ComplaintBase",
    "ComplaintCreate",
    "ComplaintUpdate",
    "ComplaintResponse",
    "ComplaintListResponse",
    "AttachmentBase",
    "AttachmentCreate",
    "AttachmentResponse",
    "RiskAssessmentBase",
    "RiskAssessmentCreate",
    "RiskAssessmentUpdate",
    "RiskAssessmentResponse",
    "AILogBase",
    "AILogCreate",
    "AILogResponse",
    "ComplaintHistoryBase",
    "ComplaintHistoryCreate",
    "ComplaintHistoryResponse",
    "CAPABase",
    "CAPACreate",
    "CAPAUpdate",
    "CAPAResponse",
    "CAPATaskBase",
    "CAPATaskCreate",
    "CAPATaskUpdate",
    "CAPATaskResponse",
]
