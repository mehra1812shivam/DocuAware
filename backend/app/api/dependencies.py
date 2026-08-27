from collections.abc import Generator

from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from app.core.security import decode_access_token, oauth2_scheme
from fastapi.security import HTTPAuthorizationCredentials
from app.models import User
from functools import lru_cache
from app.services.chat.chat_service import ChatService
from app.services.summary.summary_service import SummaryService

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        user_id = UUID(decode_access_token(token))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

def get_current_admin_user(
    user: User = Depends(get_current_user)
):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

@lru_cache
def get_chat_service() -> ChatService:
    return ChatService()

@lru_cache
def get_summary_service() -> SummaryService:
    return SummaryService()