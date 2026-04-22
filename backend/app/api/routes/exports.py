import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from openpyxl import Workbook

from app.api.routes.items import ITEMS_DB

router = APIRouter()

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


@router.get("/items/export")
def export_items():
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

    for item in ITEMS_DB:
        sheet.append([
            item["id"],
            item["title"],
            item["price"],
            item["quantity"],
            item["size"],
            item["color"],
            item["notes"],
            item["front_image_path"],
            item["back_image_path"],
        ])

    file_path = os.path.join(EXPORT_DIR, "items.xlsx")
    workbook.save(file_path)

    return FileResponse(
        path=file_path,
        filename="items.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )