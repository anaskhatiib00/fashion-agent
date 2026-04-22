import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.item import Item

router = APIRouter()

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


@router.get("/items/export")
def export_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Items"

    sheet.append([
        "ID",
        "Title",
        "Price",
        "Quantity",
        "Size",
        "Color",
        "Notes",
        "Front Image Path",
        "Back Image Path",
    ])

    for item in items:
        sheet.append([
            item.id,
            item.title,
            item.price,
            item.quantity,
            item.size,
            item.color,
            item.notes,
            item.front_image_path,
            item.back_image_path,
        ])

    file_path = os.path.join(EXPORT_DIR, "items.xlsx")
    workbook.save(file_path)

    return FileResponse(
        path=file_path,
        filename="items.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )