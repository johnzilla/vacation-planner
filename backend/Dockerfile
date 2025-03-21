# Backend Dockerfile for Vacation Planner
# This is a basic setup for running the FastAPI app in a Docker container.
# Customize as needed for production (e.g., add multi-stage build, optimize dependencies).

# Use official Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the app with uvicorn
# Note: The actual command is overridden in docker-compose.yml to run initialization scripts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Notes:
# - For production, consider adding health checks, logging, and a non-root user.
# - The initialization scripts (initialize_db.py and add_sample_holidays.py) are run
#   via the command in docker-compose.yml before starting the server.
