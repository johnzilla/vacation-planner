# API Specification

## Endpoints
- **GET /suggestions**
  - Query Params: `user_id`, `year`, `no_single_days`, `max_vacations`
  - Response: `{ "schedule": [...], "warning": "string|null" }`
- **POST /time-budget**
  - Body: `{ "accrued_days": float, "used_days": float }`
  - Response: `{ "message": "string", "accrued_days": float, "used_days": float }`
- **GET /time-budget**
  - Query Param: `user_id`
  - Response: `{ "accrued_days": float, "used_days": float }`
- **POST /holidays**
  - Body: `{ "date": "YYYY-MM-DD", "name": "string", "employer_id": int, "year": int, "country": "string" }`
  - Response: Holiday object
- **GET /employers**
  - Response: List of `{ "id": int, "name": "string" }`# API Specification

## Endpoints
- **GET /suggestions**
  - Query Params: `user_id`, `year`, `no_single_days`, `max_vacations`
  - Response: `{ "schedule": [...], "warning": "string|null" }`
- **POST /time-budget**
  - Body: `{ "accrued_days": float, "used_days": float }`
  - Response: `{ "message": "string", "accrued_days": float, "used_days": float }`
- **GET /time-budget**
  - Query Param: `user_id`
  - Response: `{ "accrued_days": float, "used_days": float }`
- **POST /holidays**
  - Body: `{ "date": "YYYY-MM-DD", "name": "string", "employer_id": int, "year": int, "country": "string" }`
  - Response: Holiday object
- **GET /employers**
  - Response: List of `{ "id": int, "name": "string" }`
