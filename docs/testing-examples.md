# Testing Examples for Vacation Planner

This document provides example test configurations and test cases to help implement testing for the Vacation Planner application.

## Backend Testing Setup

### Example pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
addopts = -v --cov=app --cov-report=term-missing
```

### Example conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.database import Base, get_db

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # Drop all tables after the test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Create a test client using the FastAPI app
    with TestClient(app) as test_client:
        yield test_client

    # Reset the dependency override
    app.dependency_overrides = {}
```

## Example Unit Tests

### Vacation Optimizer Tests

```python
import pytest
from datetime import date
from app.services.vacation_optimizer import VacationOptimizer

def test_optimize_vacation_with_holidays():
    """Test that the optimizer correctly works with holidays."""
    # Sample holidays for 2025
    holidays = [
        {"date": date(2025, 1, 1), "name": "New Year's Day"},
        {"date": date(2025, 12, 25), "name": "Christmas Day"},
    ]

    # Create optimizer with 5 vacation days
    optimizer = VacationOptimizer(
        year=2025,
        available_days=5,
        holidays=holidays,
        no_single_days=False,
        max_vacations=None
    )

    # Get optimized schedule
    schedule = optimizer.optimize()

    # Assertions
    assert len(schedule) > 0
    # Check that holidays are not included in vacation days count
    holiday_dates = [h["date"] for h in holidays]
    vacation_days_count = sum(1 for day in schedule if day["type"] == "vacation" and day["date"] not in holiday_dates)
    assert vacation_days_count <= 5

def test_no_single_days_constraint():
    """Test that the 'no single days' constraint works correctly."""
    holidays = [
        {"date": date(2025, 1, 1), "name": "New Year's Day"},
    ]

    optimizer = VacationOptimizer(
        year=2025,
        available_days=5,
        holidays=holidays,
        no_single_days=True,
        max_vacations=None
    )

    schedule = optimizer.optimize()

    # Group vacation days
    vacation_periods = []
    current_period = []

    for i, day in enumerate(schedule):
        if day["type"] == "vacation":
            current_period.append(day)
        elif current_period:
            vacation_periods.append(current_period)
            current_period = []

    if current_period:
        vacation_periods.append(current_period)

    # Check that no vacation period is just 1 day
    for period in vacation_periods:
        assert len(period) >= 2

def test_max_vacations_constraint():
    """Test that the 'max vacations' constraint works correctly."""
    holidays = [
        {"date": date(2025, 1, 1), "name": "New Year's Day"},
        {"date": date(2025, 12, 25), "name": "Christmas Day"},
    ]

    max_vacations = 2
    optimizer = VacationOptimizer(
        year=2025,
        available_days=10,
        holidays=holidays,
        no_single_days=False,
        max_vacations=max_vacations
    )

    schedule = optimizer.optimize()

    # Count distinct vacation periods
    vacation_periods = 0
    in_vacation = False

    for day in schedule:
        if day["type"] == "vacation" and not in_vacation:
            vacation_periods += 1
            in_vacation = True
        elif day["type"] != "vacation":
            in_vacation = False

    assert vacation_periods <= max_vacations
```

## Example API Integration Tests

### Suggestions API Tests

```python
def test_get_suggestions(client, db_session):
    """Test the suggestions endpoint."""
    # Add a user, time budget, and holidays to the test database
    # (This would require setting up test data in the database)

    # Make a request to the suggestions endpoint
    response = client.get("/api/suggestions?user_id=1&year=2025")

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "schedule" in data
    assert isinstance(data["schedule"], list)

def test_suggestions_with_constraints(client, db_session):
    """Test the suggestions endpoint with constraints."""
    # Add test data to the database

    # Test with no_single_days constraint
    response = client.get("/api/suggestions?user_id=1&year=2025&no_single_days=true")
    assert response.status_code == 200
    data = response.json()

    # Verify the constraint is respected in the response
    # (This would require analyzing the schedule to ensure no single vacation days)

    # Test with max_vacations constraint
    response = client.get("/api/suggestions?user_id=1&year=2025&max_vacations=2")
    assert response.status_code == 200
    data = response.json()

    # Verify the constraint is respected in the response
    # (This would require analyzing the schedule to ensure no more than 2 vacation periods)
```

## Frontend Testing Examples

### Example Svelte Component Test

```javascript
// Using Svelte Testing Library
import { render, screen, fireEvent } from '@testing-library/svelte';
import TimeBudgetForm from '../src/routes/time-budget/+page.svelte';

describe('TimeBudgetForm', () => {
  test('renders the form correctly', () => {
    render(TimeBudgetForm);

    expect(screen.getByText('Vacation Time Budget')).toBeInTheDocument();
    expect(screen.getByLabelText('Accrued Days')).toBeInTheDocument();
    expect(screen.getByLabelText('Used Days')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save' })).toBeInTheDocument();
  });

  test('validates input correctly', async () => {
    render(TimeBudgetForm);

    const accruedDaysInput = screen.getByLabelText('Accrued Days');
    const usedDaysInput = screen.getByLabelText('Used Days');
    const saveButton = screen.getByRole('button', { name: 'Save' });

    // Test invalid input (negative days)
    await fireEvent.input(accruedDaysInput, { target: { value: '-5' } });
    await fireEvent.click(saveButton);

    expect(screen.getByText('Accrued days must be a positive number')).toBeInTheDocument();

    // Test valid input
    await fireEvent.input(accruedDaysInput, { target: { value: '20' } });
    await fireEvent.input(usedDaysInput, { target: { value: '5' } });

    // Mock API call would be tested here
  });
});
```

## Getting Started with Testing

1. Install testing dependencies:
   ```bash
   # Backend
   pip install pytest pytest-cov httpx

   # Frontend
   npm install --save-dev @testing-library/svelte jest svelte-jester
   ```

2. Create the test configuration files shown above

3. Start with a few basic tests for the most critical functionality:
   - Vacation optimizer algorithm
   - Suggestions API endpoint
   - Time budget form validation

4. Run the tests:
   ```bash
   # Backend
   cd backend
   pytest

   # Frontend
   cd frontend/web
   npm test
   ```

5. Gradually expand test coverage as the application evolves
