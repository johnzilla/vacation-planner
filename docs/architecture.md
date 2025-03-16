# Architecture

## Overview
A web and mobile app to optimize vacation schedules using holidays, policies, and time budgets.

## Components
- **Frontend**: SvelteKit (web) + Svelte with Capacitor (mobile).
- **Backend**: FastAPI, SQLite (development)/PostgreSQL (production).
- **Optimizer**: Rule-based algorithm in `services/vacation_optimizer.py`.
- **Authentication**: Basic user authentication with saved vacation plans.
- **Database**: SQLAlchemy ORM with models for users, time budgets, policies, holidays, and saved plans.

## Flow
1. User inputs time budget (`time-budget/` page).
2. Backend stores time budget in database.
3. Backend uses holidays and policy to optimize schedule (`GET /api/suggestions`).
4. Results displayed (`suggestions/` page).
5. User can save vacation plans if authenticated.

## API Configuration
- All API endpoints are prefixed with `/api` in the backend.
- Frontend uses a relative path `/api` for all requests.
- Vite dev server proxies requests from `/api/*` to `http://localhost:8000/*`.

## Database
- Development: SQLite database at `backend/vacation_planner.db`.
- Production: PostgreSQL (configured in `backend/app/models/database.py`).
- Tables are created using SQLAlchemy ORM models and initialized with `initialize_db.py`.
- Sample data is added with `add_sample_holidays.py`.

## Initialization Process
1. Create database tables with `initialize_db.py`.
2. Add default user, time budget, and policy.
3. Add sample holidays with `add_sample_holidays.py`.
4. Start backend and frontend servers.

## Diagram
[User] --> [Web/Mobile Frontend] --> [API Gateway (FastAPI)] --> [SQLite/PostgreSQL]
                                   --> [Optimizer]
                                   --> [Authentication]
                                   
