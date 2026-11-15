from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import auth, complaints

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CivicTrack AI API", version="0.1.0")

app.include_router(auth.router)
app.include_router(complaints.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}