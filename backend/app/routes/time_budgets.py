from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..services.vacation_optimizer import optimize_vacation

router = APIRouter()

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
