import holidays
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..app.models.holiday import Holiday
from ..app.models.employer import Employer
from ..app.models.database import Base, DATABASE_URL
from datetime import date

def populate_holidays(year=2025, country="US"):
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    db = Session(engine)

    # Populate employers
    employer_list = ["Acme Corp"]
    for name in employer_list:
        employer = Employer(name=name)
        db.merge(employer)
    db.commit()

    # Public holidays
    us_holidays = holidays.country_holidays(country)
    for holiday_date, name in us_holidays.items():
        if holiday_date.year == year:
            holiday = Holiday(
                date=holiday_date,
                name=name,
                country=country,
                year=year,
                type="public",
                employer_id=None
            )
            db.merge(holiday)

    # Employer holidays
    employer_holidays = {
        "Acme Corp": [
            {"date": date(year, 4, 18), "name": "Good Friday"},
            {"date": date(year, 11, 28), "name": "Day After Thanksgiving"}
        ]
    }
    for emp_name, holidays_list in employer_holidays.items():
        employer = db.query(Employer).filter(Employer.name == emp_name).first()
        for emp_holiday in holidays_list:
            holiday = Holiday(
                date=emp_holiday["date"],
                name=emp_holiday["name"],
                country=country,
                year=year,
                type="employer",
                employer_id=employer.id
            )
            db.merge(holiday)

    db.commit()
    print(f"Populated holidays for {country} {year}")

if __name__ == "__main__":
    populate_holidays()
