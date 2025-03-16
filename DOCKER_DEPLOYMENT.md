# Docker Deployment for Vacation Planner

This document provides instructions for deploying the Vacation Planner application using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vacation-planner.git
   cd vacation-planner
   ```

2. Start the application:
   ```
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Services

The Docker Compose setup includes three services:

1. **db**: PostgreSQL database
   - Port: 5432
   - Credentials: vacplan/vacationplanner
   - Database: vacation_planner

2. **backend**: FastAPI application
   - Port: 8000
   - Automatically initializes the database and adds sample holidays

3. **frontend**: SvelteKit application
   - Port: 3000
   - Configured to communicate with the backend API

## Configuration

### Environment Variables

#### Backend
- `APP_ENV`: Set to "production" to use PostgreSQL
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: PostgreSQL host (db)
- `DB_PORT`: PostgreSQL port (5432)
- `DB_NAME`: PostgreSQL database name

#### Frontend
- `VITE_API_URL`: URL of the backend API

## Data Persistence

The PostgreSQL data is stored in a Docker volume named `postgres_data`. This ensures that your data persists even if the containers are stopped or removed.

## Stopping the Application

To stop the application:
```
docker-compose down
```

To stop the application and remove the volumes (this will delete all data):
```
docker-compose down -v
```

## Troubleshooting

### Database Connection Issues
If the backend cannot connect to the database, ensure the database container is healthy:
```
docker-compose ps
```

### Viewing Logs
To view logs for a specific service:
```
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Rebuilding Containers
If you make changes to the code, rebuild the containers:
```
docker-compose build
docker-compose up -d
``` 