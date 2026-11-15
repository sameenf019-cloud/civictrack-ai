import enum

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text,
)
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    citizen = "citizen"
    admin = "admin"
    officer = "officer"


class ComplaintCategory(str, enum.Enum):
    pothole = "pothole"
    garbage = "garbage"
    water_leakage = "water_leakage"
    streetlight = "streetlight"
    other = "other"


class ComplaintStatus(str, enum.Enum):
    submitted = "submitted"
    in_review = "in_review"
    assigned = "assigned"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.citizen)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ComplaintCategory), nullable=False, default=ComplaintCategory.other)
    status = Column(Enum(ComplaintStatus), nullable=False, default=ComplaintStatus.submitted, index=True)
    priority = Column(Enum(Priority), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_path = Column(String(255), nullable=True)
    citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )