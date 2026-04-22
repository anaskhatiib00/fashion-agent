import os
import shutil
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.item import Item
from app.services.ai import generate_caption

router = APIRouter()

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
    db: Session = Depends(get_db),
):
    if not front_image.content_type or not front_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Front image must be an image file")

    if not back_image.content_type or not back_image.content_type.startswith("image/"):
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

    item = Item(
        id=item_id,
        title=title,
        price=price,
        quantity=quantity,
        size=size,
        color=color,
        notes=notes,
        front_image_path=front_path,
        back_image_path=back_path,
        ai_output=None,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    try:
        ai_result = generate_caption(
            {
                "title": title,
                "price": price,
                "quantity": quantity,
                "size": size,
                "color": color,
                "notes": notes,
            }
        )
        item.ai_output = ai_result
        db.commit()
        db.refresh(item)
    except Exception as error:
        item.ai_output = f"AI generation failed: {str(error)}"
        db.commit()
        db.refresh(item)

    return {
        "message": "Item created successfully",
        "item": {
            "id": item.id,
            "title": item.title,
            "price": item.price,
            "quantity": item.quantity,
            "size": item.size,
            "color": item.color,
            "notes": item.notes,
            "front_image_path": item.front_image_path,
            "back_image_path": item.back_image_path,
            "ai_output": item.ai_output,
        },
    }


@router.get("/items")
def list_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()

    return {
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "price": item.price,
                "quantity": item.quantity,
                "size": item.size,
                "color": item.color,
                "notes": item.notes,
                "front_image_path": item.front_image_path,
                "back_image_path": item.back_image_path,
                "ai_output": item.ai_output,
            }
            for item in items
        ]
    }