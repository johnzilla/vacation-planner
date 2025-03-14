from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from .database import Base

class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    type = Column(Enum('public', 'employer', name='holiday_type'), nullable=False)
    employer_id = Column(Integer, ForeignKey("employers.id", ondelete="SET NULL"), nullable=True)from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from .database import Base

class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    type = Column(Enum('public', 'employer', name='holiday_type'), nullable=False)
    employer_id = Column(Integer, ForeignKey("employers.id", ondelete="SET NULL"), nullable=True)
