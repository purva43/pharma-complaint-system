"""
Import all routers for easy access.
"""

from app.routers.auth import router as auth_router
from app.routers.complaints import router as complaints_router
from app.routers.products import router as products_router
from app.routers.attachments import router as attachments_router
from app.routers.ai import router as ai_router

__all__ = [
    "auth_router",
    "complaints_router",
    "products_router",
    "attachments_router",
    "ai_router",
]
