"""
AI router for AI-powered complaint processing.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.ai_service import AIService
from app.middleware.auth import get_current_active_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/ai", tags=["AI"])


class AIProcessRequest(BaseModel):
    """Request model for AI processing."""
    complaint_id: str
    document_content: str


class AIProcessResponse(BaseModel):
    """Response model for AI processing."""
    success: bool
    message: str
    results: Optional[dict] = None


@router.post("/process", response_model=AIProcessResponse)
async def process_complaint_with_ai(
    request: AIProcessRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Process a complaint through the AI workflow.
    """
    try:
        results = await AIService.process_complaint(
            complaint_id=request.complaint_id,
            document_content=request.document_content,
            db=db
        )
        
        return AIProcessResponse(
            success=True,
            message="Complaint processed successfully with AI",
            results={
                "extracted_fields": results["extracted_fields"],
                "risk_assessment": results["risk_assessment"],
                "category": results["category"],
                "summary": results["summary"],
                "duplicates": results["duplicates"],
                "root_causes": results["root_causes"],
                "capa_recommendations": results["capa_recommendations"],
                "completeness": results["completeness"],
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI processing failed: {str(e)}"
        )


@router.get("/logs/{complaint_id}")
async def get_ai_logs(
    complaint_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all AI processing logs for a complaint.
    """
    try:
        logs = AIService.get_ai_logs(complaint_id, db)
        return {
            "complaint_id": complaint_id,
            "logs": [
                {
                    "node_name": log.node_name,
                    "confidence_score": float(log.confidence_score) if log.confidence_score else None,
                    "processing_time_ms": log.processing_time_ms,
                    "model_used": log.model_used,
                    "error_message": log.error_message,
                    "created_at": log.created_at.isoformat(),
                }
                for log in logs
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve AI logs: {str(e)}"
        )
