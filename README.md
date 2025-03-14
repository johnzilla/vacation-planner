# Vacation Planner

A cross-platform app to optimize employee vacation schedules based on holidays, employer policies, and accrued time budgets. Built with FastAPI (backend) and Svelte (frontend), deployable as a web app and mobile app.

## Features
- **Holiday Integration**: Pre-compiled US federal and employer-specific holidays for 2025.
- **Time Budget**: Users input accrued and used vacation days.
- **Vacation Policy**: Supports blackout dates and max days (configurable).
- **AI Optimization**: Suggests schedules maximizing contiguous days off, with options for:
  - "No single days off" (min 2 days per vacation).
  - "Max vacations" limit (e.g., 2 or 3 periods).
- **Cross-Platform**: Web (SvelteKit) and mobile (Svelte + Capacitor).
- **Database**: PostgreSQL with pre-populated holidays and user data.

## Tech Stack
- **Backend**: FastAPI (Python), PostgreSQL, SQLAlchemy.
- **Frontend**: Svelte (web), Svelte + Capacitor (mobile).
- **Deployment**: Vercel (web), Capacitor (mobile), Fly.io (backend).

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### Backend
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set up PostgreSQL:
   - Create a database: `createdb vacation_planner`.
   - Update `DATABASE_URL` in `backend/app/models/database.py`.
4. Populate holidays: `python scripts/populate_holidays.py --year 2025 --country US`.
5. Run: `uvicorn app.main:app --reload`.

### Frontend (Web)
1. Navigate to `frontend/web/`.
2. Install dependencies: `npm install`.
3. Run: `npm run dev`.

### Frontend (Mobile)
1. Navigate to `frontend/mobile/`.
2. Install dependencies: `npm install`.
3. Build web assets: `cd ../web && npm run build`.
4. Sync with Capacitor: `npx cap sync`.
5. Open in Xcode/Android Studio: `npx cap open ios` or `npx cap open android`.

## Deployment
- **Web**: Deploy to Vercel (`deploy/web/vercel.json`).
- **Mobile**: Build with Capacitor (`deploy/mobile/capacitor-deploy.sh`).
- **Backend**: Deploy to Fly.io (`deploy/backend/fly.toml`).

## Documentation
- **Architecture**: `docs/architecture.md`
- **API Spec**: `docs/api.md`
- **Database Schema**: `docs/database.md`

## License
Licensed under the Apache 2.0 License. See `LICENSE` for details.

## Contributing
- Open issues/PRs on GitHub.
- Ensure tests pass (`backend/tests/` - placeholder).
- Follow the architecture in `docs/`.

## Getting Started
1. Clone the repo: `git clone https://github.com/yourusername/vacation-planner.git`.
2. Follow setup instructions above.
3. Visit `http://localhost:5173` (web) or run the mobile app.# Vacation Planner

A cross-platform app to optimize employee vacation schedules based on holidays, employer policies, and accrued time budgets. Built with FastAPI (backend) and Svelte (frontend), deployable as a web app and mobile app.

## Features
- **Holiday Integration**: Pre-compiled US federal and employer-specific holidays for 2025.
- **Time Budget**: Users input accrued and used vacation days.
- **Vacation Policy**: Supports blackout dates and max days (configurable).
- **AI Optimization**: Suggests schedules maximizing contiguous days off, with options for:
  - "No single days off" (min 2 days per vacation).
  - "Max vacations" limit (e.g., 2 or 3 periods).
- **Cross-Platform**: Web (SvelteKit) and mobile (Svelte + Capacitor).
- **Database**: PostgreSQL with pre-populated holidays and user data.

## Tech Stack
- **Backend**: FastAPI (Python), PostgreSQL, SQLAlchemy.
- **Frontend**: Svelte (web), Svelte + Capacitor (mobile).
- **Deployment**: Vercel (web), Capacitor (mobile), Fly.io (backend).

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### Backend
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set up PostgreSQL:
   - Create a database: `createdb vacation_planner`.
   - Update `DATABASE_URL` in `backend/app/models/database.py`.
4. Populate holidays: `python scripts/populate_holidays.py --year 2025 --country US`.
5. Run: `uvicorn app.main:app --reload`.

### Frontend (Web)
1. Navigate to `frontend/web/`.
2. Install dependencies: `npm install`.
3. Run: `npm run dev`.

### Frontend (Mobile)
1. Navigate to `frontend/mobile/`.
2. Install dependencies: `npm install`.
3. Build web assets: `cd ../web && npm run build`.
4. Sync with Capacitor: `npx cap sync`.
5. Open in Xcode/Android Studio: `npx cap open ios` or `npx cap open android`.

## Deployment
- **Web**: Deploy to Vercel (`deploy/web/vercel.json`).
- **Mobile**: Build with Capacitor (`deploy/mobile/capacitor-deploy.sh`).
- **Backend**: Deploy to Fly.io (`deploy/backend/fly.toml`).

## Documentation
- **Architecture**: `docs/architecture.md`
- **API Spec**: `docs/api.md`
- **Database Schema**: `docs/database.md`

## License
Licensed under the Apache 2.0 License. See `LICENSE` for details.

## Contributing
- Open issues/PRs on GitHub.
- Ensure tests pass (`backend/tests/` - placeholder).
- Follow the architecture in `docs/`.

## Getting Started
1. Clone the repo: `git clone https://github.com/yourusername/vacation-planner.git`.
2. Follow setup instructions above.
3. Visit `http://localhost:5173` (web) or run the mobile app.
