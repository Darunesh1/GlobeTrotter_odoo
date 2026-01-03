from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Base schema with common attributes
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


# Schema for user registration
class UserCreate(UserBase):
    password: str


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for updating user profile
class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None


# Schema for user response (what API returns)
class UserResponse(UserBase):
    id: int
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows SQLAlchemy model to Pydantic conversion


# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Schema for token data
class TokenData(BaseModel):
    user_id: Optional[int] = None
