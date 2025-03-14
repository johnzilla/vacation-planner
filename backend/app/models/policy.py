from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    max_days = Column(Integer, nullable=False)
    blackout_dates = Column(JSON)  # List of dates
    created_at = Column(DateTime, server_default=func.now())
  
