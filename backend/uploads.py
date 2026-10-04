from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4

from backend.database import get_connection

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads" / "products"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


@router.post("/api/products/{product_id}/images")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are allowed."
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM products WHERE id = ?",
        (product_id,)
    )
    product = cursor.fetchone()

    if product is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Product not found.")

    image_data = await file.read(MAX_FILE_SIZE + 1)

    if not image_data:
        connection.close()
        raise HTTPException(status_code=400, detail="The image is empty.")

    if len(image_data) > MAX_FILE_SIZE:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="Image must be 5 MB or smaller."
        )

    extension = ALLOWED_TYPES[file.content_type]
    filename = f"{uuid4().hex}{extension}"
    image_path = UPLOAD_DIR / filename

    try:
        image_path.write_bytes(image_data)

        relative_path = f"uploads/products/{filename}"

        cursor.execute(
            """
            INSERT INTO product_images (product_id, image_path)
            VALUES (?, ?)
            """,
            (product_id, relative_path)
        )

        connection.commit()

    except Exception:
        if image_path.exists():
            image_path.unlink()
        connection.close()
        raise HTTPException(
            status_code=500,
            detail="Image could not be saved."
        )

    connection.close()

    return {
        "status": "success",
        "message": "Product image uploaded successfully.",
        "product_id": product_id,
        "image_path": relative_path
    }