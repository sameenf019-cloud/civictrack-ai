from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import ComplaintCategory, ComplaintStatus, Priority, UserRole


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ComplaintCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10, max_length=2000)
    category: ComplaintCategory = ComplaintCategory.other
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class ComplaintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category: ComplaintCategory
    status: ComplaintStatus
    priority: Priority | None
    latitude: float
    longitude: float
    image_path: str | None
    citizen_id: int
    officer_id: int | None
    created_at: datetime
    

class AssignRequest(BaseModel):
    officer_id: int


class StatusUpdate(BaseModel):
    status: ComplaintStatus