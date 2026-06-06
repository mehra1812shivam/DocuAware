from sqlalchemy.orm import Session

from app.schemas.user import UserRegister

from app.models import User

from fastapi import HTTPException, status

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token
)

class UserService:

    @staticmethod
    def create_user(
        db: Session,
        user_data: UserRegister
    ):
        existing_user = db.query(User).filter(
            User.email == user_data.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_password = get_password_hash(
            user_data.password
        )
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            department=user_data.department
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ):
        user = db.query(User).filter(
            User.email == email
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not verify_password(password,user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )        
        access_token = create_access_token(subject=str(user.id))

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }