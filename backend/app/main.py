from fastapi import FastAPI
from .routes import suggestions, time_budgets, holidays

app = FastAPI(
    title="Vacation Planner",
    description="API for optimizing vacation schedules",
    version="1.0.0"
)

# Include routers
app.include_router(suggestions.router, prefix="/api")
app.include_router(time_budgets.router, prefix="/api")
app.include_router(holidays.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Vacation Planner API"}
  
