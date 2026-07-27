"""
Authentication service for business logic.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash, verify_password


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def create_user(user_data: UserCreate, db: Session) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            db: Database session
            
        Returns:
            User: Created user
        """
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def authenticate_user(email: str, password: str, db: Session) -> User | None:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User email
            password: Plain text password
            db: Database session
            
        Returns:
            User: Authenticated user if credentials are valid, None otherwise
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
