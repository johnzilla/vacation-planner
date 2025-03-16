from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import suggestions, time_budgets, holidays, auth, saved_plans

app = FastAPI(
    title="Vacation Planner",
    description="API for optimizing vacation schedules",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(suggestions.router, prefix="/api")
app.include_router(time_budgets.router, prefix="/api")
app.include_router(holidays.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(saved_plans.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Vacation Planner API"}
  
