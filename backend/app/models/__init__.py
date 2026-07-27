"""
Import all models for SQLAlchemy to recognize them.
"""

from app.models.user import User, UserRole
from app.models.product import Product
from app.models.complaint import Complaint, ComplaintStatus, ComplaintPriority, RiskLevel
from app.models.attachment import Attachment
from app.models.risk_assessment import RiskAssessment
from app.models.ai_log import AILog
from app.models.complaint_history import ComplaintHistory
from app.models.capa import CAPA, CAPAType, CAPAStatus
from app.models.capa_task import CAPATask, TaskStatus

__all__ = [
    "User",
    "UserRole",
    "Product",
    "Complaint",
    "ComplaintStatus",
    "ComplaintPriority",
    "RiskLevel",
    "Attachment",
    "RiskAssessment",
    "AILog",
    "ComplaintHistory",
    "CAPA",
    "CAPAType",
    "CAPAStatus",
    "CAPATask",
    "TaskStatus",
]
