from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.exports import router as exports_router
from app.api.routes.items import router as items_router
from app.core.database import Base, engine
from app.models import Item

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fashion Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router, prefix="/api")
app.include_router(exports_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Fashion Agent API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}