# System Patterns

2025-03-22 20:02:10 - Updated with implemented patterns.

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.
2025-03-22 19:53:00 - Log of updates made.

## Coding Patterns

* **Backend API Structure**: FastAPI routers organized by feature area (auth, holidays, suggestions, etc.)
* **Database Models**: SQLAlchemy ORM models with clear relationships
* **Frontend Routes**: SvelteKit routes corresponding to main application features
* **Authentication**: JWT-based authentication with token storage

## Architectural Patterns

* **API-First Design**: Backend API designed with clear endpoints and documentation
* **Service Layer**: Business logic encapsulated in services (e.g., vacation_optimizer.py)
* **Cross-Platform Strategy**: Shared business logic with platform-specific UI implementations
* **Environment-Based Configuration**: Different database configurations for development vs. production

## Testing Patterns

* **Test Directory Structure**: Separate directories for unit and integration tests (currently empty)
* **Recommended Test Approach**:
  - Unit tests for core business logic (vacation optimizer)
  - Integration tests for API endpoints
  - Frontend component tests for UI elements

## Recommended Development Patterns

* **Code Quality**:
  - Python: flake8 for linting, black for formatting
  - JavaScript/Svelte: ESLint with Prettier
  - Pre-commit hooks for automated formatting

* **CI/CD Pipeline**:
  - GitHub Actions for automated testing and building
  - Docker-based deployment for consistency

* **Documentation**:
  - Markdown-based documentation in docs/ directory

## Implemented Development Patterns

* **Testing Strategy**:
  - Unit tests for core business logic (vacation optimizer)
  - Integration tests for API endpoints
  - Test fixtures for database mocking
  - Coverage reporting with pytest-cov

* **Code Quality**:
  - Python: flake8 for linting, black for formatting, isort for import sorting
  - JavaScript/Svelte: ESLint with Prettier
  - EditorConfig for consistent editor settings
  - Pre-commit hooks for automated checks

* **Environment Configuration**:
  - .env files for environment-specific settings
  - Example files for documentation
  - Setup script for development environment initialization

* **CI/CD Pipeline**:
  - GitHub Actions for automated testing and linting
  - Separate jobs for backend and frontend
  - Build verification for the frontend

  - OpenAPI/Swagger for API documentation
  - JSDoc/docstrings for code documentation
