from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from jose import jwt,JWTError

from app.core.config import settings

from app.schemas.user import TokenPayload

from fastapi.security import OAuth2PasswordBearer,HTTPBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = HTTPBearer()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str,hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject,"exp": expire}
    
    token = jwt.encode(
    payload,
    settings.jwt_secret,
    algorithm=settings.jwt_algorithm
    )

    return token

def decode_access_token(token: str) -> str:
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm]
    )

    token_data = TokenPayload(**payload)
    return token_data.sub

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")