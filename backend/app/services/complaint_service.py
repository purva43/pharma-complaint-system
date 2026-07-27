"""
Complaint service for business logic.
"""

from sqlalchemy.orm import Session
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate
from app.utils.validators import generate_complaint_no
from datetime import date


class ComplaintService:
    """Service for complaint operations."""
    
    @staticmethod
    def create_complaint(complaint_data: ComplaintCreate, user_id: str, db: Session) -> Complaint:
        """
        Create a new complaint.
        
        Args:
            complaint_data: Complaint creation data
            user_id: User ID creating the complaint
            db: Database session
            
        Returns:
            Complaint: Created complaint
        """
        year = date.today().year
        complaint_no = generate_complaint_no(year, 1)
        
        new_complaint = Complaint(
            complaint_no=complaint_no,
            user_id=user_id,
            created_by=user_id,
            **complaint_data.model_dump(exclude_unset=True)
        )
        
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)
        return new_complaint
    
    @staticmethod
    def update_complaint(complaint_id: str, complaint_data: ComplaintUpdate, user_id: str, db: Session) -> Complaint:
        """
        Update an existing complaint.
        
        Args:
            complaint_id: Complaint ID
            complaint_data: Complaint update data
            user_id: User ID updating the complaint
            db: Database session
            
        Returns:
            Complaint: Updated complaint
        """
        complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
        
        if not complaint:
            raise ValueError("Complaint not found")
        
        update_data = complaint_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(complaint, field, value)
        
        complaint.updated_by = user_id
        
        db.commit()
        db.refresh(complaint)
        return complaint
