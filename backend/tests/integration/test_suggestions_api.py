from datetime import date

# pytest is used implicitly by the fixtures
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.holiday import Holiday
from app.models.policy import Policy
from app.models.time_budget import TimeBudget
from app.models.user import User


def test_get_suggestions(client: TestClient, db_session: Session):
    """Test the suggestions endpoint."""
    # Create test data
    user = User(email="test@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()

    policy = Policy(user_id=user.id, max_days=30, blackout_dates=[])
    db_session.add(policy)

    time_budget = TimeBudget(user_id=user.id, accrued_days=10, used_days=0)
    db_session.add(time_budget)

    # Add some holidays
    holidays = [
        Holiday(
            date=date(2025, 1, 1),
            name="New Year's Day",
            year=2025,
            country="US",
            type="public",
        ),
        Holiday(
            date=date(2025, 12, 25),
            name="Christmas Day",
            year=2025,
            country="US",
            type="public",
        ),
    ]
    for holiday in holidays:
        db_session.add(holiday)

    db_session.commit()

    # Make a request to the suggestions endpoint
    response = client.get(f"/api/suggestions?user_id={user.id}&year=2025")

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "schedule" in data
    assert isinstance(data["schedule"], list)

    # Should have at least one vacation period
    assert len(data["schedule"]) > 0

    # Total days used should not exceed available days
    total_days_used = sum(period["days_used"] for period in data["schedule"])
    assert total_days_used <= time_budget.accrued_days - time_budget.used_days


def test_suggestions_with_no_single_days(client: TestClient, db_session: Session):
    """Test the suggestions endpoint with no_single_days constraint."""
    # Create test data
    user = User(email="test2@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()

    policy = Policy(user_id=user.id, max_days=30, blackout_dates=[])
    db_session.add(policy)

    time_budget = TimeBudget(user_id=user.id, accrued_days=10, used_days=0)
    db_session.add(time_budget)

    # Add some holidays
    holidays = [
        Holiday(
            date=date(2025, 1, 1),
            name="New Year's Day",
            year=2025,
            country="US",
            type="public",
        )
    ]
    for holiday in holidays:
        db_session.add(holiday)

    db_session.commit()

    # Make a request to the suggestions endpoint with no_single_days=true
    response = client.get(f"/api/suggestions?user_id={user.id}&year=2025&no_single_days=true")

    # Check the response
    assert response.status_code == 200
    data = response.json()

    # Verify the constraint is respected in the response
    for period in data["schedule"]:
        start = period["start"]
        end = period["end"]
        # Check that the period is at least 2 days
        # (This is a simplified check - in reality, we'd need to count workdays)
        assert start != end


def test_suggestions_with_max_vacations(client: TestClient, db_session: Session):
    """Test the suggestions endpoint with max_vacations constraint."""
    # Create test data
    user = User(email="test3@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()

    policy = Policy(user_id=user.id, max_days=30, blackout_dates=[])
    db_session.add(policy)

    time_budget = TimeBudget(user_id=user.id, accrued_days=10, used_days=0)
    db_session.add(time_budget)

    # Add some holidays
    holidays = [
        Holiday(
            date=date(2025, 1, 1),
            name="New Year's Day",
            year=2025,
            country="US",
            type="public",
        ),
        Holiday(
            date=date(2025, 7, 4),
            name="Independence Day",
            year=2025,
            country="US",
            type="public",
        ),
        Holiday(
            date=date(2025, 12, 25),
            name="Christmas Day",
            year=2025,
            country="US",
            type="public",
        ),
    ]
    for holiday in holidays:
        db_session.add(holiday)

    db_session.commit()

    # Make a request to the suggestions endpoint with max_vacations=2
    response = client.get(f"/api/suggestions?user_id={user.id}&year=2025&max_vacations=2")

    # Check the response
    assert response.status_code == 200
    data = response.json()

    # Verify the constraint is respected in the response
    assert len(data["schedule"]) <= 2


def test_suggestions_with_invalid_user(client: TestClient, db_session: Session):
    """Test the suggestions endpoint with an invalid user ID."""
    # Make a request with a non-existent user ID
    response = client.get("/api/suggestions?user_id=999&year=2025")

    # Should return an error
    assert response.status_code == 404
