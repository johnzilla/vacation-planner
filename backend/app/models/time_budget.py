from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class TimeBudget(Base):
    __tablename__ = "time_budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    accrued_days = Column(Float, nullable=False)
    used_days = Column(Float, default=0.0)
    updated_at = Column(DateTime, server_default=func.now())from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class TimeBudget(Base):
    __tablename__ = "time_budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    accrued_days = Column(Float, nullable=False)
    used_days = Column(Float, default=0.0)
    updated_at = Column(DateTime, server_default=func.now())
