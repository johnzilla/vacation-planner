from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.holiday import Holiday
from ..models.employer import Employer
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class HolidayCreate(BaseModel):
    date: date
    name: str
    employer_id: int
    year: int
    country: str = "US"

@router.post("/holidays")
def add_holiday(holiday: HolidayCreate, db: Session = Depends(get_db)):
    employer = db.query(Employer).filter(Employer.id == holiday.employer_id).first()
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    new_holiday = Holiday(
        date=holiday.date,
        name=holiday.name,
        country=holiday.country,
        year=holiday.year,
        type="employer",
        employer_id=holiday.employer_id
    )
    db.add(new_holiday)
    db.commit()
    db.refresh(new_holiday)
    return new_holiday

@router.get("/employers")
def get_employers(db: Session = Depends(get_db)):
    return db.query(Employer).all()
