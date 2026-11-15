from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models
from app.database import Base, engine
from app.routers import auth, complaints, images
from app.routers.images import UPLOAD_DIR

Base.metadata.create_all(bind=engine)
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="CivicTrack AI API", version="0.1.0")

app.include_router(auth.router)
app.include_router(complaints.router)
app.include_router(images.router)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/health")
def health_check():
    return {"status": "ok"}