from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class SavedPlan(Base):
    __tablename__ = "saved_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    year = Column(Integer, nullable=False)
    schedule = Column(JSON, nullable=False)  # Store the vacation schedule as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_public = Column(Integer, default=0)  # 0 = private, 1 = public/shareable
    share_token = Column(String, nullable=True, unique=True)  # For sharing with non-registered users 