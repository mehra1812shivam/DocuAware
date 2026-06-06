from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from app.core.enums import Department,UserRole


class UserRegister(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    department: Department

class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: UUID
    name: str
    email: EmailStr
    department: Department
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    sub: str