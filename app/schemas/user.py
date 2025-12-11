from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

from app.models.enums import GenderEnum


class UserProfileCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    info: Optional[str] = None


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    info: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]
    gender: Optional[GenderEnum]
    date_of_birth: Optional[date]
    info: Optional[str]

    class Config:
        from_attributes = True
