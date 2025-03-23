from datetime import date, datetime, timedelta

from app.models.holiday import Holiday
from app.models.policy import Policy
from app.models.time_budget import TimeBudget
from app.services.vacation_optimizer import generate_period, optimize_vacation

# pytest is used implicitly by the fixtures


class TestGeneratePeriod:
    def test_generate_period_basic(self):
        """Test basic period generation with no constraints."""
        start_date = date(2025, 1, 6)  # Monday
        end_date = date(2025, 1, 10)  # Friday
        holiday_dates = {}
        blackout_dates = set()
        available_days = 5
        no_single_days = False

        periods = generate_period(
            start_date,
            end_date,
            holiday_dates,
            blackout_dates,
            available_days,
            no_single_days,
            skip_date_check=True,
        )

        assert len(periods) == 1
        period = periods[0]
        assert period["start_date"] == start_date
        assert period["end_date"] == end_date
        assert period["days_used"] == 5  # 5 workdays
        assert period["total_days_off"] == 5  # No weekends or holidays
        assert period["workdays"] == 5
        assert period["holidays"] == 0
        assert period["weekends"] == 0
        assert len(period["dates"]) == 5

    def test_generate_period_with_weekend(self):
        """Test period generation that includes a weekend."""
        start_date = date(2025, 1, 3)  # Friday
        end_date = date(2025, 1, 6)  # Monday
        holiday_dates = {}
        blackout_dates = set()
        available_days = 5
        no_single_days = False

        periods = generate_period(
            start_date,
            end_date,
            holiday_dates,
            blackout_dates,
            available_days,
            no_single_days,
            skip_date_check=True,
        )

        assert len(periods) == 1
        period = periods[0]
        assert period["days_used"] == 2  # Friday and Monday
        assert period["total_days_off"] == 4  # 2 workdays + 2 weekend days
        assert period["workdays"] == 2
        assert period["holidays"] == 0
        assert period["weekends"] == 2

    def test_generate_period_with_holiday(self):
        """Test period generation that includes a holiday."""
        start_date = date(2025, 1, 1)  # New Year's Day (Wednesday)
        end_date = date(2025, 1, 3)  # Friday
        holiday_dates = {date(2025, 1, 1): Holiday(date=date(2025, 1, 1), name="New Year's Day")}
        blackout_dates = set()
        available_days = 5
        no_single_days = False

        periods = generate_period(
            start_date,
            end_date,
            holiday_dates,
            blackout_dates,
            available_days,
            no_single_days,
            skip_date_check=True,
        )

        assert len(periods) == 1
        period = periods[0]
        assert period["days_used"] == 2  # Thursday and Friday
        assert period["total_days_off"] == 3  # 2 workdays + 1 holiday
        assert period["workdays"] == 2
        assert period["holidays"] == 1
        assert period["weekends"] == 0

    def test_generate_period_with_blackout_date(self):
        """Test period generation with a blackout date."""
        start_date = date(2025, 1, 6)  # Monday
        end_date = date(2025, 1, 10)  # Friday
        holiday_dates = {}
        blackout_dates = {date(2025, 1, 8)}  # Wednesday is blackout
        available_days = 5
        no_single_days = False

        periods = generate_period(
            start_date,
            end_date,
            holiday_dates,
            blackout_dates,
            available_days,
            no_single_days,
            skip_date_check=True,
        )

        assert len(periods) == 1
        period = periods[0]
        assert period["days_used"] == 4  # 4 workdays (excluding Wednesday)
        assert period["total_days_off"] == 4

    def test_generate_period_no_single_days(self):
        """Test period generation with no_single_days constraint."""
        # Test a single day period
        start_date = date(2025, 1, 6)  # Monday
        end_date = date(2025, 1, 6)  # Monday
        holiday_dates = {}
        blackout_dates = set()
        available_days = 5
        no_single_days = True

        periods = generate_period(
            start_date,
            end_date,
            holiday_dates,
            blackout_dates,
            available_days,
            no_single_days,
            skip_date_check=True,
        )

        # Should return empty list because period is too short
        assert len(periods) == 0

        # Test a two-day period
        start_date = date(2025, 1, 6)  # Monday
        end_date = date(2025, 1, 7)  # Tuesday

        periods = generate_period(
            start_date,
            end_date,
            holiday_dates,
            blackout_dates,
            available_days,
            no_single_days,
            skip_date_check=True,
        )

        # Should return a period
        assert len(periods) == 1
        assert periods[0]["days_used"] == 2

    def test_generate_period_too_many_days(self):
        """Test period generation when more workdays than available days."""
        start_date = date(2025, 1, 6)  # Monday
        end_date = date(2025, 1, 10)  # Friday
        holiday_dates = {}
        blackout_dates = set()
        available_days = 3  # Only 3 days available
        no_single_days = False

        periods = generate_period(
            start_date,
            end_date,
            holiday_dates,
            blackout_dates,
            available_days,
            no_single_days,
            skip_date_check=True,
        )

        # Should return empty list because not enough available days
        assert len(periods) == 0


# Mock classes for testing optimize_vacation
class MockDB:
    def __init__(self, policy, time_budget, holidays):
        self.policy = policy
        self.time_budget = time_budget
        self.holidays = holidays

    def query(self, model):
        if model == Policy:
            return MockQuery(self.policy)
        elif model == TimeBudget:
            return MockQuery(self.time_budget)
        elif model == Holiday:
            return MockQuery(self.holidays)
        return MockQuery(None)


class MockQuery:
    def __init__(self, result):
        self.result = result

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        if isinstance(self.result, list):
            return self.result[0] if self.result else None
        return self.result

    def all(self):
        if isinstance(self.result, list):
            return self.result
        return [self.result] if self.result else []


class TestOptimizeVacation:
    def test_optimize_vacation_basic(self):
        """Test basic vacation optimization."""
        # Create mock data
        user_id = 1
        year = 2025

        policy = Policy(id=1, user_id=user_id, max_days=30, blackout_dates=[])

        time_budget = TimeBudget(id=1, user_id=user_id, accrued_days=10, used_days=0)

        holidays = [
            Holiday(id=1, date=date(2025, 1, 1), name="New Year's Day", year=2025),
            Holiday(id=2, date=date(2025, 12, 25), name="Christmas Day", year=2025),
        ]

        # Create mock DB
        db = MockDB(policy, time_budget, holidays)

        # Call optimize_vacation
        result = optimize_vacation(user_id, year, db)

        # Basic assertions
        assert "schedule" in result
        assert isinstance(result["schedule"], list)

        # Should have at least one vacation period
        assert len(result["schedule"]) > 0

        # Total days used should not exceed available days
        total_days_used = sum(period["days_used"] for period in result["schedule"])
        assert total_days_used <= time_budget.accrued_days - time_budget.used_days

    def test_optimize_vacation_no_single_days(self):
        """Test vacation optimization with no single days constraint."""
        # Create mock data
        user_id = 1
        year = 2025

        policy = Policy(id=1, user_id=user_id, max_days=30, blackout_dates=[])

        time_budget = TimeBudget(id=1, user_id=user_id, accrued_days=10, used_days=0)

        holidays = [Holiday(id=1, date=date(2025, 1, 1), name="New Year's Day", year=2025)]

        # Create mock DB
        db = MockDB(policy, time_budget, holidays)

        # Call optimize_vacation with no_single_days=True
        result = optimize_vacation(user_id, year, db, no_single_days=True)

        # Check that no vacation period is just 1 day
        for period in result["schedule"]:
            start = datetime.strptime(period["start"], "%Y-%m-%d").date()
            end = datetime.strptime(period["end"], "%Y-%m-%d").date()
            assert (end - start).days >= 1

    def test_optimize_vacation_max_vacations(self):
        """Test vacation optimization with max vacations constraint."""
        # Create mock data
        user_id = 1
        year = 2025

        policy = Policy(id=1, user_id=user_id, max_days=30, blackout_dates=[])

        time_budget = TimeBudget(id=1, user_id=user_id, accrued_days=10, used_days=0)

        holidays = [
            Holiday(id=1, date=date(2025, 1, 1), name="New Year's Day", year=2025),
            Holiday(id=2, date=date(2025, 7, 4), name="Independence Day", year=2025),
            Holiday(id=3, date=date(2025, 12, 25), name="Christmas Day", year=2025),
        ]

        # Create mock DB
        db = MockDB(policy, time_budget, holidays)

        # Call optimize_vacation with max_vacations=2
        result = optimize_vacation(user_id, year, db, max_vacations=2)

        # Should have at most 2 vacation periods
        assert len(result["schedule"]) <= 2

    def test_optimize_vacation_blackout_dates(self):
        """Test vacation optimization with blackout dates."""
        # Create mock data
        user_id = 1
        year = 2025

        policy = Policy(
            id=1,
            user_id=user_id,
            max_days=30,
            blackout_dates=[
                "2025-06-01",
                "2025-06-02",
                "2025-06-03",
            ],  # Blackout first week of June
        )

        time_budget = TimeBudget(id=1, user_id=user_id, accrued_days=10, used_days=0)

        holidays = [Holiday(id=1, date=date(2025, 1, 1), name="New Year's Day", year=2025)]

        # Create mock DB
        db = MockDB(policy, time_budget, holidays)

        # Call optimize_vacation
        result = optimize_vacation(user_id, year, db)

        # Check that no vacation period includes blackout dates
        blackout_dates = {datetime.strptime(d, "%Y-%m-%d").date() for d in policy.blackout_dates}
        for period in result["schedule"]:
            start = datetime.strptime(period["start"], "%Y-%m-%d").date()
            end = datetime.strptime(period["end"], "%Y-%m-%d").date()

            current = start
            while current <= end:
                assert current not in blackout_dates
                current += timedelta(days=1)
