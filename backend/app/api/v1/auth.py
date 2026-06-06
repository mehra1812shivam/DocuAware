from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db
from app.schemas.user import (
    UserRegister,
    UserResponse,
    UserLogin,
    Token
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",response_model=UserResponse,status_code=201)
def register(user_data: UserRegister,db: Session = Depends(get_db)):
    return UserService.create_user(
        db=db,
        user_data=user_data
    )

@router.post("/login",response_model=Token)
def login(user_data: UserLogin,db: Session = Depends(get_db)):
    return UserService.authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password
    )