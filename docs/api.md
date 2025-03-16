# API Specification

## Base URL
All endpoints are prefixed with `/api` in the backend.

## Endpoints

### Vacation Suggestions
- **GET /api/suggestions**
  - Query Params: `user_id`, `year` (default: 2025), `no_single_days` (default: false), `max_vacations` (optional)
  - Response: `{ "schedule": [...], "warning": "string|null" }`
  - Description: Returns optimized vacation suggestions based on holidays, policy, and time budget.

### Time Budget
- **POST /api/time-budget**
  - Body: `{ "user_id": int, "accrued_days": float, "used_days": float }`
  - Response: `{ "id": int, "user_id": int, "accrued_days": float, "used_days": float, "updated_at": string }`
  - Description: Updates a user's time budget.
  
- **GET /api/time-budget**
  - Query Param: `user_id`
  - Response: `{ "id": int, "user_id": int, "accrued_days": float, "used_days": float, "updated_at": string }`
  - Description: Returns a user's current time budget.

### Holidays
- **POST /api/holidays**
  - Body: `{ "date": "YYYY-MM-DD", "name": "string", "employer_id": int, "year": int, "country": "string", "type": "public|employer" }`
  - Response: Holiday object
  - Description: Adds a new holiday to the database.

### Authentication
- **POST /api/auth/register**
  - Body: `{ "email": "string", "password": "string" }`
  - Response: `{ "id": int, "email": "string", "token": "string" }`
  - Description: Registers a new user.
  
- **POST /api/auth/login**
  - Body: `{ "email": "string", "password": "string" }`
  - Response: `{ "id": int, "email": "string", "token": "string" }`
  - Description: Authenticates a user and returns a token.

### Saved Plans
- **GET /api/saved-plans**
  - Headers: `Authorization: Bearer <token>`
  - Response: List of saved plan objects
  - Description: Returns all saved plans for the authenticated user.
  
- **POST /api/saved-plans**
  - Headers: `Authorization: Bearer <token>`
  - Body: `{ "name": "string", "year": int, "schedule": object, "is_public": boolean }`
  - Response: Saved plan object
  - Description: Creates a new saved plan.
  
- **GET /api/saved-plans/{id}**
  - Headers: `Authorization: Bearer <token>` (optional if plan is public)
  - Response: Saved plan object
  - Description: Returns a specific saved plan.
  
- **PUT /api/saved-plans/{id}**
  - Headers: `Authorization: Bearer <token>`
  - Body: `{ "name": "string", "year": int, "schedule": object, "is_public": boolean }`
  - Response: Updated saved plan object
  - Description: Updates a saved plan.
  
- **DELETE /api/saved-plans/{id}**
  - Headers: `Authorization: Bearer <token>`
  - Response: `{ "message": "Plan deleted successfully" }`
  - Description: Deletes a saved plan.
  
- **POST /api/saved-plans/{id}/share**
  - Headers: `Authorization: Bearer <token>`
  - Response: `{ "share_token": "string" }`
  - Description: Creates a share token for a saved plan.
  
- **GET /api/saved-plans/shared/{token}**
  - Response: Shared plan object
  - Description: Returns a shared plan using a share token.
