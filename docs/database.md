# Database Schema

## Tables
- **users**: `id`, `email`, `password_hash`, `created_at`
- **time_budgets**: `id`, `user_id`, `accrued_days`, `used_days`, `updated_at`
- **holidays**: `id`, `date`, `name`, `country`, `year`, `type (public/employer)`, `employer_id` (no foreign key)
- **saved_plans**: `id`, `user_id`, `name`, `year`, `vacation_days`, `is_public`, `share_token`, `created_at`

## Database Configuration
- Development: SQLite database at `backend/vacation_planner.db`
- Production: PostgreSQL (configured in `backend/app/models/database.py`)

## Initialization
Database tables are created using the `init_db.py` script in the backend directory.
