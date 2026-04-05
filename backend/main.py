from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.score_engine import process_economy, get_demo_economies, get_economy_data

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="OAKCRED.GLOBAL - Macro Engine", version="1.0.0")

# Mount frontend directory for direct access
# This allows visitng http://18.61.166.88:8000/ to see the dashboard
app.mount("/dashboard", StaticFiles(directory="../frontend"), name="dashboard")

@app.get("/")
def read_root():
    return FileResponse("../frontend/index.html")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For demo, allow all. Update to Amplify URL in Production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EconomyEvaluate(BaseModel):
    iso_code: str
    overrides: dict = {}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/economies")
def list_economies():
    try:
        return {"status": "success", "data": get_demo_economies()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/score")
def evaluate_economy(data: EconomyEvaluate):
    try:
        # Get real data from snapshot
        base_data = get_economy_data(data.iso_code)
        if not base_data:
            raise HTTPException(status_code=404, detail="Economy data not found")
        
        # Apply any "Simulator" overrides (for Policy scenario testing)
        eval_data = {**base_data, **data.overrides}
        
        # Process and calculate macro resilience score + SHAP
        result = process_economy(eval_data)
        return {"status": "success", "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/login")
def login(credentials: dict):
    # Dummy auth for demo
    email = credentials.get("email")
    pwd = credentials.get("password")
    if pwd == "demo123":
        if email == "applicant@demo.com": role = "applicant" # Evaluator
        elif email == "officer@demo.com": role = "officer" # Policy Analyst
        elif email == "admin@demo.com": role = "admin" # System Admin
        else: return {"status": "error", "message": "Invalid email"}
        
        return {"access_token": f"fake-jwt-{role}", "role": role}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Ensure required run logic if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
