import os
import shutil
import uuid

from fastapi import APIRouter, File, Form, UploadFile, HTTPException

router = APIRouter()

ITEMS_DB = []

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/items")
async def create_item(
    title: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    size: str = Form(...),
    color: str = Form(...),
    notes: str = Form(""),
    front_image: UploadFile = File(...),
    back_image: UploadFile = File(...),
):
    if not front_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Front image must be an image file")

    if not back_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Back image must be an image file")

    item_id = str(uuid.uuid4())

    front_filename = f"{item_id}_front_{front_image.filename}"
    back_filename = f"{item_id}_back_{back_image.filename}"

    front_path = os.path.join(UPLOAD_DIR, front_filename)
    back_path = os.path.join(UPLOAD_DIR, back_filename)

    with open(front_path, "wb") as buffer:
        shutil.copyfileobj(front_image.file, buffer)

    with open(back_path, "wb") as buffer:
        shutil.copyfileobj(back_image.file, buffer)

    item = {
        "id": item_id,
        "title": title,
        "price": price,
        "quantity": quantity,
        "size": size,
        "color": color,
        "notes": notes,
        "front_image_path": front_path,
        "back_image_path": back_path,
    }

    ITEMS_DB.append(item)

    return {
        "message": "Item created successfully",
        "item": item,
    }


@router.get("/items")
def list_items():
    return {"items": ITEMS_DB}