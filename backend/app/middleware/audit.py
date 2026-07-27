"""
Audit logging middleware for complaint change tracking.
"""

from sqlalchemy.orm import Session
from app.models.complaint_history import ComplaintHistory
from datetime import datetime


async def log_complaint_change(
    db: Session,
    complaint_id: str,
    action: str,
    changed_by: str,
    reason: str = None,
    field_changed: str = None,
    old_value: str = None,
    new_value: str = None
):
    """
    Log a complaint change to the audit trail.
    
    Args:
        db: Database session
        complaint_id: UUID of the complaint
        action: Action performed (create, update, delete, etc.)
        changed_by: UUID of the user who made the change
        reason: Optional reason for the change
        field_changed: Optional name of the field that changed
        old_value: Optional old value before change
        new_value: Optional new value after change
    """
    history_entry = ComplaintHistory(
        complaint_id=complaint_id,
        action=action,
        field_changed=field_changed,
        old_value=old_value,
        new_value=new_value,
        changed_by=changed_by,
        reason=reason,
        created_at=datetime.utcnow()
    )
    
    db.add(history_entry)
    db.commit()
