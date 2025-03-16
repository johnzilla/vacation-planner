# API Specification

## Base URL
All endpoints are prefixed with `/api` in the backend.

## Endpoints

### Vacation Suggestions
- **GET /api/suggestions**
  - Query Params: `user_id`, `year`, `no_single_days`, `max_vacations`
  - Response: `{ "schedule": [...], "warning": "string|null" }`

### Time Budget
- **POST /api/time-budget**
  - Body: `{ "user_id": int, "accrued_days": float, "used_days": float }`
  - Response: `{ "id": int, "user_id": int, "accrued_days": float, "used_days": float, "updated_at": string }`
- **GET /api/time-budget**
  - Query Param: `user_id`
  - Response: `{ "id": int, "user_id": int, "accrued_days": float, "used_days": float, "updated_at": string }`

### Holidays
- **POST /api/holidays**
  - Body: `{ "date": "YYYY-MM-DD", "name": "string", "employer_id": int, "year": int, "country": "string", "type": "public|employer" }`
  - Response: Holiday object

### Authentication
- **POST /api/auth/register**
  - Body: `{ "email": "string", "password": "string" }`
  - Response: `{ "id": int, "email": "string", "token": "string" }`
- **POST /api/auth/login**
  - Body: `{ "email": "string", "password": "string" }`
  - Response: `{ "id": int, "email": "string", "token": "string" }`

### Saved Plans
- **GET /api/saved-plans**
  - Headers: `Authorization: Bearer <token>`
  - Response: List of saved plan objects
- **POST /api/saved-plans**
  - Headers: `Authorization: Bearer <token>`
  - Body: `{ "name": "string", "year": int, "vacation_days": [string], "is_public": boolean }`
  - Response: Saved plan object
- **GET /api/saved-plans/{id}**
  - Headers: `Authorization: Bearer <token>` (optional if plan is public)
  - Response: Saved plan object
- **PUT /api/saved-plans/{id}**
  - Headers: `Authorization: Bearer <token>`
  - Body: `{ "name": "string", "year": int, "vacation_days": [string], "is_public": boolean }`
  - Response: Updated saved plan object
- **DELETE /api/saved-plans/{id}**
  - Headers: `Authorization: Bearer <token>`
  - Response: `{ "message": "Plan deleted successfully" }`
- **POST /api/saved-plans/{id}/share**
  - Headers: `Authorization: Bearer <token>`
  - Response: `{ "share_token": "string" }`
- **GET /api/saved-plans/shared/{token}**
  - Response: Shared plan object
