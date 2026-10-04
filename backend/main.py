from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import initialize_database
app = FastAPI(
    title="JK Safety Vision API",
    description="Backend system for JK Safety Vision",
    version="1.0.0"
)
initialize_database()
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
@app.get("/api/products")
def get_products():
    from backend.database import get_connection

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return {
        "status": "success",
        "products": products
    }