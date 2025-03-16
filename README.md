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
- **Database**: SQLite for development, PostgreSQL for production.
- **Authentication**: User authentication and saved vacation plans.

## Tech Stack
- **Backend**: FastAPI (Python), SQLite/PostgreSQL, SQLAlchemy.
- **Frontend**: SvelteKit (web), Svelte + Capacitor (mobile).
- **Deployment**: Vercel (web), Capacitor (mobile), Fly.io (backend), Docker (full stack).

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+ (for production only)

### Backend
1. Navigate to `backend/`.
2. Create a virtual environment: `python -m venv venv` and activate it:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`.
4. Initialize the database and create sample data:
   ```
   python initialize_db.py     # Creates tables and default user/policy/time-budget
   python add_sample_holidays.py  # Adds 2025 US holidays
   ```
5. Run: `uvicorn app.main:app --reload`.

### Frontend (Web)
1. Navigate to `frontend/web/`.
2. Install dependencies: `npm install`.
3. Run: `npm run dev`.
4. Access the application at `http://localhost:5173`.

### Frontend (Mobile)
1. Navigate to `frontend/mobile/`.
2. Install dependencies: `npm install`.
3. Build web assets: `cd ../web && npm run build`.
4. Sync with Capacitor: `npx cap sync`.
5. Open in Xcode/Android Studio: `npx cap open ios` or `npx cap open android`.

### Docker Deployment (Recommended for Production)
For a complete deployment with PostgreSQL, backend, and frontend:

1. Make sure Docker and Docker Compose are installed.
2. Run: `docker-compose up -d`
3. Access the application at http://localhost:3000

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed instructions.

## API Configuration
The frontend is configured to proxy API requests to the backend:
- In development, API requests are proxied from `/api/*` to `http://localhost:8000/*`.
- The API base URL is set to `/api` in `frontend/web/src/lib/api.js`.

## Database Configuration
- Development: SQLite database at `backend/vacation_planner.db`.
- Production: PostgreSQL (configure in `backend/app/models/database.py`).

## Database Initialization
The application requires several database tables and initial data:
1. **Users**: Default user with ID 1 is created by `initialize_db.py`.
2. **Time Budget**: Default time budget with 20 accrued days is created.
3. **Policy**: Default policy with max 30 days and no blackout dates is created.
4. **Holidays**: Sample 2025 US holidays are added by `add_sample_holidays.py`.

## Deployment
- **Web**: Deploy to Vercel (`deploy/web/vercel.json`).
- **Mobile**: Build with Capacitor (`deploy/mobile/capacitor-deploy.sh`).
- **Backend**: Deploy to Fly.io (`deploy/backend/fly.toml`).
- **Full Stack**: Deploy with Docker Compose (see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)).

## Documentation
- **Architecture**: `docs/architecture.md`
- **API Spec**: `docs/api.md`
- **Database Schema**: `docs/database.md`
- **Docker Deployment**: `DOCKER_DEPLOYMENT.md`
- **Roadmap**: `docs/roadmap.md`

## License
Licensed under the Apache License, Version 2.0. See the following files for details:
- `LICENSE`: The full Apache 2.0 license text
- `COPYRIGHT`: Copyright notice
- `NOTICE`: Attribution notices for third-party components

## Contributing
- Open issues/PRs on GitHub.
- Ensure tests pass (`backend/tests/` - placeholder).
- Follow the architecture in `docs/`.

## Getting Started
1. Clone the repo: `git clone https://github.com/yourusername/vacation-planner.git`.
2. Follow setup instructions above.
3. Visit `http://localhost:5173` (web) or run the mobile app.

## Troubleshooting
- If you encounter database errors, ensure you've run `python initialize_db.py` in the backend directory.
- For API 404 errors, check that both backend and frontend servers are running.
- The Vite dev server proxies API requests to the backend - ensure the proxy configuration in `frontend/web/vite.config.js` is correct.
- If no vacation suggestions appear, make sure you've added holidays with `python add_sample_holidays.py`.
