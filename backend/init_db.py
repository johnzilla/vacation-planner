from app.models.database import init_db, Base, engine

if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
