from app.models.database import init_db, Base, engine
# Import all models to ensure they are registered with SQLAlchemy
from app.models.user import User
from app.models.time_budget import TimeBudget
from app.models.holiday import Holiday
from app.models.saved_plan import SavedPlan
from app.models.policy import Policy

if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
