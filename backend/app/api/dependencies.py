from collections.abc import Generator

from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from app.core.security import decode_access_token, oauth2_scheme
from fastapi.security import HTTPAuthorizationCredentials
from app.models import User

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