# Database Schema

## Tables
- **users**: `id`, `email`, `password_hash`, `created_at`
- **time_budgets**: `id`, `user_id`, `accrued_days`, `used_days`, `updated_at`
- **holidays**: `id`, `date`, `name`, `country`, `year`, `type (public/employer)`, `employer_id` (no foreign key)
- **saved_plans**: `id`, `user_id`, `name`, `year`, `schedule`, `is_public`, `share_token`, `created_at`, `updated_at`
- **policies**: `id`, `user_id`, `max_days`, `blackout_dates`, `created_at`

## Database Configuration
- Development: SQLite database at `backend/vacation_planner.db`
- Production: PostgreSQL (configured in `backend/app/models/database.py`)

## Initialization
Database tables and initial data are created using scripts in the backend directory:

1. **initialize_db.py**: Creates all tables and adds:
   - Default user (ID: 1, email: user@example.com)
   - Default time budget (20 accrued days, 0 used days)
   - Default policy (max 30 days, no blackout dates)

2. **add_sample_holidays.py**: Adds sample US holidays for 2025:
   - New Year's Day (Jan 1)
   - Martin Luther King Jr. Day (Jan 20)
   - Presidents' Day (Feb 17)
   - Memorial Day (May 26)
   - Independence Day (Jul 4)
   - Labor Day (Sep 1)
   - Columbus Day (Oct 13)
   - Veterans Day (Nov 11)
   - Thanksgiving Day (Nov 27)
   - Christmas Day (Dec 25)

## Data Relationships
- **User** has many **Time Budgets** (one-to-many)
- **User** has many **Policies** (one-to-many)
- **User** has many **Saved Plans** (one-to-many)
- **Holiday** can be associated with an employer (optional)
