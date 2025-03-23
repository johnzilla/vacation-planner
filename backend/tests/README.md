# Running Tests for Vacation Planner

This directory contains tests for the Vacation Planner backend.

## Setup

Make sure you have installed the development dependencies:

```bash
# From the backend directory
source venv/bin/activate
pip install pytest pytest-cov
```

## Running Tests

To run all tests:

```bash
# From the backend directory
source venv/bin/activate
pytest
```

Or use the helper script created during setup:

```bash
# From the backend directory
./run_tests.sh
```

## Running with Coverage

To run tests with coverage reporting:

```bash
# From the backend directory
source venv/bin/activate
pytest --cov=app
```

Or using the helper script:

```bash
# From the backend directory
./run_tests.sh --cov=app
```

## Test Structure

- `unit/`: Contains unit tests for individual components
  - `test_vacation_optimizer.py`: Tests for the vacation optimization algorithm

- `integration/`: Contains integration tests for API endpoints
  - `test_suggestions_api.py`: Tests for the suggestions API endpoint

## Writing New Tests

When adding new tests:

1. Place unit tests in the `unit/` directory
2. Place integration tests in the `integration/` directory
3. Name test files with the prefix `test_`
4. Name test functions with the prefix `test_`

Example:

```python
# backend/tests/unit/test_example.py

def test_example_function():
    # Test code here
    assert True
