"""
Complaint router for CRUD operations on complaints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.database import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse, ComplaintListResponse
from app.middleware.auth import get_current_active_user
from app.utils.validators import generate_complaint_no
from app.middleware.audit import log_complaint_change

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint_data: ComplaintCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new complaint.
    """
    year = date.today().year
    complaint_no = generate_complaint_no(year, 1)
    
    new_complaint = Complaint(
        complaint_no=complaint_no,
        user_id=current_user.id,
        created_by=current_user.id,
        **complaint_data.model_dump(exclude_unset=True)
    )
    
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    
    await log_complaint_change(
        db=db,
        complaint_id=str(new_complaint.id),
        action="create",
        changed_by=str(current_user.id),
        reason="Complaint created"
    )
    
    return new_complaint


@router.get("", response_model=ComplaintListResponse)
async def list_complaints(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    risk_level: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List complaints with pagination and filters.
    """
    query = db.query(Complaint).filter(Complaint.deleted_at.is_(None))
    
    if status:
        query = query.filter(Complaint.status == status)
    if priority:
        query = query.filter(Complaint.priority == priority)
    if risk_level:
        query = query.filter(Complaint.risk_level == risk_level)
    if category:
        query = query.filter(Complaint.category == category)
    
    total = query.count()
    complaints = query.offset(skip).limit(limit).all()
    
    return ComplaintListResponse(
        items=complaints,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific complaint by ID.
    """
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.deleted_at.is_(None)
    ).first()
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
async def update_complaint(
    complaint_id: str,
    complaint_data: ComplaintUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a complaint.
    """
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.deleted_at.is_(None)
    ).first()
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    update_data = complaint_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(complaint, field, value)
    
    complaint.updated_by = current_user.id
    
    db.commit()
    db.refresh(complaint)
    
    await log_complaint_change(
        db=db,
        complaint_id=complaint_id,
        action="update",
        changed_by=str(current_user.id),
        reason="Complaint updated"
    )
    
    return complaint


@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_complaint(
    complaint_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete a complaint.
    """
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.deleted_at.is_(None)
    ).first()
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    from datetime import datetime
    complaint.deleted_at = datetime.utcnow()
    
    db.commit()
    
    await log_complaint_change(
        db=db,
        complaint_id=complaint_id,
        action="delete",
        changed_by=str(current_user.id),
        reason="Complaint deleted"
    )
