# Architecture

## Overview
A web and mobile app to optimize vacation schedules using holidays, policies, and time budgets.

## Components
- **Frontend**: SvelteKit (web) + Svelte with Capacitor (mobile).
- **Backend**: FastAPI, SQLite (development)/PostgreSQL (production).
- **Optimizer**: Rule-based algorithm in `services/vacation_optimizer.py`.
- **Authentication**: Basic user authentication with saved vacation plans.

## Flow
1. User inputs time budget (`time-budget/` page).
2. User adds employer holidays (`holidays/` page).
3. Backend optimizes schedule (`GET /api/suggestions`).
4. Results displayed (`suggestions/` page).
5. User can save vacation plans if authenticated.

## API Configuration
- All API endpoints are prefixed with `/api` in the backend.
- Frontend uses a relative path `/api` for all requests.
- Vite dev server proxies requests from `/api/*` to `http://localhost:8000/*`.

## Database
- Development: SQLite database at `backend/vacation_planner.db`.
- Production: PostgreSQL (configured in `backend/app/models/database.py`).
- Tables are created using SQLAlchemy ORM models and initialized with `init_db.py`.

## Diagram
[User] --> [Web/Mobile Frontend] --> [API Gateway (FastAPI)] --> [SQLite/PostgreSQL]
                                   --> [Optimizer]
                                   --> [Authentication]
                                   
