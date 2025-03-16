from app.models.database import SessionLocal
from app.models.holiday import Holiday
from datetime import date

def add_sample_holidays():
    db = SessionLocal()
    try:
        # Check if holidays already exist for 2025
        existing_holidays = db.query(Holiday).filter(Holiday.year == 2025).count()
        if existing_holidays > 0:
            print(f"{existing_holidays} holidays already exist for 2025")
            return
        
        # Sample US holidays for 2025
        holidays = [
            # New Year's Day
            Holiday(date=date(2025, 1, 1), name="New Year's Day", country="US", year=2025, type="public"),
            
            # Martin Luther King Jr. Day (3rd Monday in January)
            Holiday(date=date(2025, 1, 20), name="Martin Luther King Jr. Day", country="US", year=2025, type="public"),
            
            # Presidents' Day (3rd Monday in February)
            Holiday(date=date(2025, 2, 17), name="Presidents' Day", country="US", year=2025, type="public"),
            
            # Memorial Day (Last Monday in May)
            Holiday(date=date(2025, 5, 26), name="Memorial Day", country="US", year=2025, type="public"),
            
            # Independence Day
            Holiday(date=date(2025, 7, 4), name="Independence Day", country="US", year=2025, type="public"),
            
            # Labor Day (1st Monday in September)
            Holiday(date=date(2025, 9, 1), name="Labor Day", country="US", year=2025, type="public"),
            
            # Columbus Day (2nd Monday in October)
            Holiday(date=date(2025, 10, 13), name="Columbus Day", country="US", year=2025, type="public"),
            
            # Veterans Day
            Holiday(date=date(2025, 11, 11), name="Veterans Day", country="US", year=2025, type="public"),
            
            # Thanksgiving Day (4th Thursday in November)
            Holiday(date=date(2025, 11, 27), name="Thanksgiving Day", country="US", year=2025, type="public"),
            
            # Christmas Day
            Holiday(date=date(2025, 12, 25), name="Christmas Day", country="US", year=2025, type="public"),
        ]
        
        # Add holidays to the database
        db.add_all(holidays)
        db.commit()
        print(f"Added {len(holidays)} sample holidays for 2025")
        
    except Exception as e:
        db.rollback()
        print(f"Error adding sample holidays: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_holidays() 