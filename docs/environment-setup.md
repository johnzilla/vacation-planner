# Environment Setup Guide

This document provides guidance on setting up environment variables and configuration for the Vacation Planner application.

## Environment Variables

The application uses environment variables for configuration in different environments (development, production). Below are the recommended environment variables for each component.

### Backend Environment Variables

Create a `.env.example` file in the `backend/` directory with the following content:

```dotenv
# Application Environment
APP_ENV=development  # Options: development, production

# Database Configuration
# For SQLite (development)
# No additional configuration needed, uses vacation_planner.db by default

# For PostgreSQL (production)
DB_USER=vacplan
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacation_planner

# Authentication
SECRET_KEY=your_secret_key_for_jwt_tokens
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_PREFIX=/api
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Frontend Environment Variables

Create a `.env.example` file in the `frontend/web/` directory with the following content:

```dotenv
# API Configuration
VITE_API_URL=http://localhost:8000/api

# Feature Flags
VITE_ENABLE_AUTH=true
VITE_ENABLE_SHARING=true

# Analytics (future use)
VITE_ANALYTICS_ID=

# Deployment
VITE_APP_ENV=development  # Options: development, production
```

## Setup Script

Create a `setup-dev.sh` script in the root directory to help set up the development environment:

```bash
#!/bin/bash
# Setup script for Vacation Planner development environment

echo "Setting up Vacation Planner development environment..."

# Create backend .env file if it doesn't exist
if [ ! -f backend/.env ]; then
  echo "Creating backend/.env file..."
  cp backend/.env.example backend/.env
  echo "Please update backend/.env with your specific configuration."
else
  echo "backend/.env already exists."
fi

# Create frontend .env file if it doesn't exist
if [ ! -f frontend/web/.env ]; then
  echo "Creating frontend/web/.env file..."
  cp frontend/web/.env.example frontend/web/.env
  echo "Please update frontend/web/.env with your specific configuration."
else
  echo "frontend/web/.env already exists."
fi

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend/web
npm install
cd ../..

# Initialize database
echo "Initializing database..."
cd backend
source venv/bin/activate
python initialize_db.py
python add_sample_holidays.py
cd ..

echo "Setup complete! You can now start the application:"
echo "Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "Frontend: cd frontend/web && npm run dev"
```

## Environment-Specific Configuration

### Development Environment

In development:
- Backend uses SQLite database
- Frontend proxies API requests to the backend
- CORS is configured to allow requests from the frontend development server

### Production Environment

In production:
- Backend uses PostgreSQL database
- Frontend is built as a static site
- API requests are configured based on deployment setup
- CORS is configured to allow only specific origins

## Database Configuration

The database configuration is handled in `backend/app/models/database.py`. The application uses SQLite for development and PostgreSQL for production, determined by the `APP_ENV` environment variable.

Example database configuration:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get environment variables
APP_ENV = os.getenv("APP_ENV", "development")

if APP_ENV == "production":
    # PostgreSQL for production
    DB_USER = os.getenv("DB_USER", "vacplan")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "vacationplanner")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "vacation_planner")

    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # SQLite for development
    SQLALCHEMY_DATABASE_URL = "sqlite:///./vacation_planner.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Docker Environment Configuration

When using Docker, environment variables are set in the `docker-compose.yml` file. The Docker setup uses PostgreSQL by default.

## Best Practices

1. **Never commit sensitive information**:
   - Add `.env` files to `.gitignore`
   - Only commit `.env.example` files with placeholder values

2. **Use different values for different environments**:
   - Development: Simple, local configuration
   - Production: Secure, optimized configuration

3. **Document all environment variables**:
   - Keep this guide updated with all required variables
   - Include comments explaining each variable's purpose

4. **Validate environment variables**:
   - Check for required variables on application startup
   - Provide clear error messages when variables are missing
