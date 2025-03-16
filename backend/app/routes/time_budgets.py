from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..models.database import get_db
from ..models.time_budget import TimeBudget
from ..services.vacation_optimizer import optimize_vacation

router = APIRouter()

class TimeBudgetUpdate(BaseModel):
    user_id: int
    accrued_days: float
    used_days: float

@router.get("/suggestions")
def get_suggestions(
    user_id: int,
    year: int = 2025,
    no_single_days: bool = False,
    max_vacations: int = None,
    db: Session = Depends(get_db)
):
    result = optimize_vacation(user_id, year, no_single_days, max_vacations, db)
    return result

@router.get("/time-budget")
def get_time_budget(user_id: int, db: Session = Depends(get_db)):
    time_budget = db.query(TimeBudget).filter(TimeBudget.user_id == user_id).first()
    if not time_budget:
        # Create a default time budget if none exists
        time_budget = TimeBudget(user_id=user_id, accrued_days=0.0, used_days=0.0)
        db.add(time_budget)
        db.commit()
        db.refresh(time_budget)
    return time_budget

@router.post("/time-budget")
def update_time_budget(budget: TimeBudgetUpdate, db: Session = Depends(get_db)):
    time_budget = db.query(TimeBudget).filter(TimeBudget.user_id == budget.user_id).first()
    if not time_budget:
        time_budget = TimeBudget(
            user_id=budget.user_id,
            accrued_days=budget.accrued_days,
            used_days=budget.used_days
        )
        db.add(time_budget)
    else:
        time_budget.accrued_days = budget.accrued_days
        time_budget.used_days = budget.used_days
    
    db.commit()
    db.refresh(time_budget)
    return time_budget
