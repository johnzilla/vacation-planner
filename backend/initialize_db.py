from app.models.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.time_budget import TimeBudget
from app.models.policy import Policy
import hashlib

def initialize_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if user already exists
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            # Create default user
            password_hash = hashlib.sha256("password123".encode()).hexdigest()
            user = User(
                id=1,
                email="user@example.com",
                password_hash=password_hash
            )
            db.add(user)
            db.commit()
            print("Default user created successfully")
        else:
            print("Default user already exists")
        
        # Check if time budget exists
        time_budget = db.query(TimeBudget).filter(TimeBudget.user_id == 1).first()
        if not time_budget:
            # Create default time budget
            time_budget = TimeBudget(
                user_id=1,
                accrued_days=20.0,
                used_days=0.0
            )
            db.add(time_budget)
            db.commit()
            print("Default time budget created successfully")
        else:
            print("Time budget already exists")
        
        # Check if policy exists
        policy = db.query(Policy).filter(Policy.user_id == 1).first()
        if not policy:
            # Create default policy
            policy = Policy(
                user_id=1,
                max_days=30,
                blackout_dates=[]
            )
            db.add(policy)
            db.commit()
            print("Default policy created successfully")
        else:
            print("Policy already exists")
            
        print("Database initialization completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database() 