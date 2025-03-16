from app.models.database import SessionLocal
from app.models.user import User
import hashlib

def create_default_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.id == 1).first()
        if existing_user:
            print("User with ID 1 already exists")
            return
        
        # Create a simple password hash (in production, use a proper password hashing library)
        password_hash = hashlib.sha256("password123".encode()).hexdigest()
        
        # Create default user
        default_user = User(
            id=1,  # Force ID to be 1
            email="user@example.com",
            password_hash=password_hash
        )
        
        db.add(default_user)
        db.commit()
        print("Default user created successfully with ID 1")
    except Exception as e:
        db.rollback()
        print(f"Error creating default user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_user() 