from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.database import get_db
from ..models.policy import Policy
from ..models.time_budget import TimeBudget
from ..services.vacation_optimizer import optimize_vacation

router = APIRouter()


@router.get("/suggestions")
def get_suggestions(
    user_id: int,
    year: int = 2025,
    no_single_days: bool = False,
    max_vacations: int = None,
    db: Session = Depends(get_db),
):
    # Check if user exists by looking for their time budget and policy
    time_budget = db.query(TimeBudget).filter(TimeBudget.user_id == user_id).first()
    policy = db.query(Policy).filter(Policy.user_id == user_id).first()

    if not time_budget or not policy:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    result = optimize_vacation(user_id, year, db, no_single_days, max_vacations)
    return result
