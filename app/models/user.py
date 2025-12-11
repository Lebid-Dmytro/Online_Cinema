from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum as SQLEnum, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base
from app.models.enums import UserGroupEnum, GenderEnum


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(SQLEnum(UserGroupEnum), unique=True, nullable=False, index=True)

    users = relationship("User", back_populates="group")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    group_id = Column(Integer, ForeignKey("user_groups.id"), nullable=False)

    group = relationship("UserGroup", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    gender = Column(SQLEnum(GenderEnum), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    info = Column(Text, nullable=True)

    user = relationship("User", back_populates="profile")
