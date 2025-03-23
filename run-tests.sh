#!/bin/bash
# Helper script to run tests for Vacation Planner

# Check if we're in the project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "Error: This script must be run from the project root directory."
    exit 1
fi

# Function to display help
show_help() {
    echo "Usage: ./run-tests.sh [options]"
    echo ""
    echo "Options:"
    echo "  --backend       Run backend tests only (default if no option specified)"
    echo "  --frontend      Run frontend tests only"
    echo "  --all           Run both backend and frontend tests"
    echo "  --coverage      Run tests with coverage reporting"
    echo "  --help          Display this help message"
    echo ""
    echo "Examples:"
    echo "  ./run-tests.sh                  # Run backend tests"
    echo "  ./run-tests.sh --backend        # Run backend tests"
    echo "  ./run-tests.sh --frontend       # Run frontend tests"
    echo "  ./run-tests.sh --all            # Run all tests"
    echo "  ./run-tests.sh --coverage       # Run backend tests with coverage"
    echo "  ./run-tests.sh --all --coverage # Run all tests with coverage"
}

# Default values
run_backend=true
run_frontend=false
coverage=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend)
            run_backend=true
            run_frontend=false
            shift
            ;;
        --frontend)
            run_backend=false
            run_frontend=true
            shift
            ;;
        --all)
            run_backend=true
            run_frontend=true
            shift
            ;;
        --coverage)
            coverage=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Run backend tests
if [ "$run_backend" = true ]; then
    echo "Running backend tests..."
    cd backend

    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "Warning: Virtual environment not found. Creating one..."
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    fi

    # Run tests
    if [ "$coverage" = true ]; then
        pytest --cov=app
    else
        pytest
    fi

    # Deactivate virtual environment
    deactivate
    cd ..
    echo "Backend tests completed."
fi

# Run frontend tests
if [ "$run_frontend" = true ]; then
    echo "Running frontend tests..."
    cd frontend/web

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "Warning: Node modules not found. Installing dependencies..."
        npm install
    fi

    # Run tests
    if [ "$coverage" = true ]; then
        npm test -- --coverage
    else
        npm test
    fi

    cd ../..
    echo "Frontend tests completed."
fi

echo "All tests completed."
