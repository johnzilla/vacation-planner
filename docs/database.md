# Database Schema

## Tables
- **users**: `id`, `email`, `password_hash`, `created_at`
- **policies**: `id`, `user_id`, `max_days`, `blackout_dates (JSONB)`, `created_at`
- **time_budgets**: `id`, `user_id`, `accrued_days`, `used_days`, `updated_at`
- **employers**: `id`, `name`, `created_at`
- **holidays**: `id`, `date`, `name`, `country`, `year`, `type (public/employer)`, `employer_id`
