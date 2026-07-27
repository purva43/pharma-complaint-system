"""
AI service for processing complaints with LangGraph workflow.
"""

from sqlalchemy.orm import Session
from app.models.complaint import Complaint
from app.models.ai_log import AILog
from app.ai.langgraph_workflow import process_complaint_with_ai
from datetime import datetime
import json


class AIService:
    """Service for AI-powered complaint processing."""
    
    @staticmethod
    async def process_complaint(complaint_id: str, document_content: str, db: Session) -> dict:
        """
        Process a complaint through the AI workflow.
        
        Args:
            complaint_id: UUID of the complaint
            document_content: Raw document content
            db: Database session
            
        Returns:
            dict: Complete AI processing results
        """
        result = await process_complaint_with_ai(complaint_id, document_content)
        
        for log in result["ai_logs"]:
            ai_log = AILog(
                complaint_id=complaint_id,
                node_name=log["node_name"],
                input_data=log.get("input_data"),
                output_data=log.get("output_data"),
                confidence_score=log.get("confidence_score"),
                processing_time_ms=log.get("processing_time_ms"),
                model_used=log.get("model_used"),
                error_message=log.get("error_message"),
                created_at=datetime.utcnow()
            )
            db.add(ai_log)
        
        db.commit()
        
        complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
        if complaint:
            if result["extracted_fields"]:
                if result["extracted_fields"].get("description"):
                    complaint.description = result["extracted_fields"]["description"]
                if result["extracted_fields"].get("reporter_name"):
                    complaint.reporter_name = result["extracted_fields"]["reporter_name"]
                if result["extracted_fields"].get("reporter_email"):
                    complaint.reporter_email = result["extracted_fields"]["reporter_email"]
                if result["extracted_fields"].get("reporter_phone"):
                    complaint.reporter_phone = result["extracted_fields"]["reporter_phone"]
                if result["extracted_fields"].get("batch_lot_no"):
                    complaint.batch_lot_no = result["extracted_fields"]["batch_lot_no"]
            
            if result["summary"].get("summary"):
                complaint.summary = result["summary"]["summary"]
            
            if result["risk_assessment"].get("risk_level"):
                complaint.risk_level = result["risk_assessment"]["risk_level"]
            
            if result["category"].get("category"):
                complaint.category = result["category"]["category"]
            
            db.commit()
            db.refresh(complaint)
        
        return result
    
    @staticmethod
    def get_ai_logs(complaint_id: str, db: Session) -> list[AILog]:
        """
        Get all AI logs for a complaint.
        
        Args:
            complaint_id: UUID of the complaint
            db: Database session
            
        Returns:
            list: AI log entries
        """
        return db.query(AILog).filter(AILog.complaint_id == complaint_id).all()
