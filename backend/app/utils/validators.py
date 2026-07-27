"""
Custom validators for data validation.
"""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (international format).
    
    Args:
        phone: Phone number string
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Accept formats: +1234567890, 123-456-7890, (123) 456-7890
    pattern = r'^\+?[\d\s\-\(\)]{10,20}$'
    return re.match(pattern, phone) is not None


def validate_batch_lot_no(batch_no: str) -> bool:
    """
    Validate batch/lot number format.
    
    Args:
        batch_no: Batch/lot number string
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Accept alphanumeric with hyphens, underscores, length 3-50
    pattern = r'^[A-Za-z0-9\-_]{3,50}$'
    return re.match(pattern, batch_no) is not None


def generate_complaint_no(year: int, sequence: int) -> str:
    """
    Generate a complaint number.
    
    Args:
        year: Current year
        sequence: Sequence number for the year
        
    Returns:
        str: Complaint number in format CMP-YYYY-XXXX
    """
    return f"CMP-{year}-{sequence:04d}"


def generate_capa_no(year: int, sequence: int) -> str:
    """
    Generate a CAPA number.
    
    Args:
        year: Current year
        sequence: Sequence number for the year
        
    Returns:
        str: CAPA number in format CAPA-YYYY-XXXX
    """
    return f"CAPA-{year}-{sequence:04d}"
