from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import initialize_database
app = FastAPI(
    title="JK Safety Vision API",
    description="Backend system for JK Safety Vision",
    version="1.0.0"
)

# Website connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "JK Safety Vision Backend is running!"
    }

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "backend": "FastAPI",
        "project": "JK Safety Vision"
    }