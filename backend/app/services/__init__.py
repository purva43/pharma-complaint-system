"""
Import all services for easy access.
"""

from app.services.auth_service import AuthService
from app.services.complaint_service import ComplaintService
from app.services.ai_service import AIService

__all__ = [
    "AuthService",
    "ComplaintService",
    "AIService",
]
