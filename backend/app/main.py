from fastapi import FastAPI

from app import models
from app.database import Base, engine

# Creates tables that do not exist yet (prototype only; we may use
# migrations later).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CivicTrack AI API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}