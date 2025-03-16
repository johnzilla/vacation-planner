from app.models.database import SessionLocal
from app.models.policy import Policy

def create_default_policy():
    db = SessionLocal()
    try:
        # Check if policy already exists for user_id 1
        existing_policy = db.query(Policy).filter(Policy.user_id == 1).first()
        if existing_policy:
            print("Policy already exists for user_id 1")
            return
        
        # Create default policy
        default_policy = Policy(
            user_id=1,
            max_days=30,  # Default max days
            blackout_dates=[]  # No blackout dates by default
        )
        
        db.add(default_policy)
        db.commit()
        print("Default policy created successfully for user_id 1")
    except Exception as e:
        db.rollback()
        print(f"Error creating default policy: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_policy() 