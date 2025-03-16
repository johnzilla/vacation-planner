from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

from ..models.database import get_db
from ..models.saved_plan import SavedPlan
from ..models.user import User
from .auth import get_current_user

router = APIRouter(tags=["saved_plans"], prefix="/saved-plans")

# Models
class SavedPlanBase(BaseModel):
    name: str
    year: int
    schedule: dict
    is_public: Optional[int] = 0

class SavedPlanCreate(SavedPlanBase):
    pass

class SavedPlanResponse(SavedPlanBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    share_token: Optional[str] = None

    class Config:
        orm_mode = True

# Routes
@router.post("/", response_model=SavedPlanResponse)
def create_saved_plan(
    plan: SavedPlanCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Create a new saved plan
    db_plan = SavedPlan(
        name=plan.name,
        user_id=current_user.id,
        year=plan.year,
        schedule=plan.schedule,
        is_public=plan.is_public
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.get("/", response_model=List[SavedPlanResponse])
def get_user_saved_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    return db.query(SavedPlan).filter(SavedPlan.user_id == current_user.id).all()

@router.get("/{plan_id}", response_model=SavedPlanResponse)
def get_saved_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    plan = db.query(SavedPlan).filter(SavedPlan.id == plan_id).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Check if the plan is public or belongs to the current user
    if plan.is_public == 0 and (current_user is None or plan.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this plan")
    
    return plan

@router.put("/{plan_id}", response_model=SavedPlanResponse)
def update_saved_plan(
    plan_id: int,
    plan_update: SavedPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    db_plan = db.query(SavedPlan).filter(SavedPlan.id == plan_id).first()
    
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    if db_plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this plan")
    
    # Update plan fields
    db_plan.name = plan_update.name
    db_plan.year = plan_update.year
    db_plan.schedule = plan_update.schedule
    db_plan.is_public = plan_update.is_public
    
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    db_plan = db.query(SavedPlan).filter(SavedPlan.id == plan_id).first()
    
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    if db_plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this plan")
    
    db.delete(db_plan)
    db.commit()
    
    return None

@router.post("/{plan_id}/share", response_model=SavedPlanResponse)
def create_share_link(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    db_plan = db.query(SavedPlan).filter(SavedPlan.id == plan_id).first()
    
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    if db_plan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to share this plan")
    
    # Generate a unique share token if one doesn't exist
    if not db_plan.share_token:
        db_plan.share_token = str(uuid.uuid4())
        db_plan.is_public = 1  # Make the plan public when shared
        db.commit()
        db.refresh(db_plan)
    
    return db_plan

@router.get("/shared/{share_token}", response_model=SavedPlanResponse)
def get_shared_plan(
    share_token: str,
    db: Session = Depends(get_db)
):
    # This endpoint is public - no authentication required
    plan = db.query(SavedPlan).filter(SavedPlan.share_token == share_token).first()
    
    if not plan or plan.is_public == 0:
        raise HTTPException(status_code=404, detail="Shared plan not found")
    
    return plan 