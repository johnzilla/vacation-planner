from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Determine which database to use based on environment
# This allows easy switching between SQLite (development) and PostgreSQL (production)
ENVIRONMENT = os.environ.get("APP_ENV", "development")

if ENVIRONMENT == "production":
    # Production PostgreSQL configuration
    DB_USER = os.environ.get("DB_USER", "vacplan")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "yourpassword")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "vacation_planner")
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    # Development SQLite configuration
    DATABASE_URL = "sqlite:///./vacation_planner.db"

# Create engine with appropriate settings
if ENVIRONMENT == "development":
    # SQLite-specific settings
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # PostgreSQL settings
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
