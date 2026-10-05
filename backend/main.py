from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.database import initialize_database, get_connection
from backend.uploads import router as uploads_router
from backend.auth import verify_password


app = FastAPI(
    title="JK Safety Vision API",
    description="Backend system for JK Safety Vision",
    version="1.0.0"
)


initialize_database()
app.include_router(uploads_router)


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


# =========================================================
# ADMIN LOGIN
# =========================================================

class AdminLogin(BaseModel):
    email: str
    password: str


@app.post("/api/admin/login")
def admin_login(login: AdminLogin):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, email, password_hash, salt
        FROM admin_users
        WHERE LOWER(email) = LOWER(?)
        """,
        (login.email,)
    )

    admin = cursor.fetchone()
    connection.close()

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = verify_password(
        login.password,
        admin["password_hash"],
        admin["salt"]
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "status": "success",
        "message": "Admin login successful",
        "admin": {
            "id": admin["id"],
            "email": admin["email"]
        }
    }


# =========================================================
# PRODUCTS
# =========================================================

@app.get("/api/products")
def get_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products ORDER BY id DESC")

    products = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return {
        "status": "success",
        "products": products
    }


class ProductCreate(BaseModel):
    name: str
    model: str = ""
    brand: str = ""
    category: str = ""
    description: str = ""
    cost_price: float = 0
    selling_price: float = 0
    discount_price: float = 0
    stock: int = 0


@app.post("/api/products")
def create_product(product: ProductCreate):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products
        (
            name,
            model,
            brand,
            category,
            description,
            cost_price,
            selling_price,
            discount_price,
            stock
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product.name,
            product.model,
            product.brand,
            product.category,
            product.description,
            product.cost_price,
            product.selling_price,
            product.discount_price,
            product.stock
        )
    )

    connection.commit()

    product_id = cursor.lastrowid

    connection.close()

    return {
        "status": "success",
        "message": "Product created successfully",
        "product_id": product_id
    }