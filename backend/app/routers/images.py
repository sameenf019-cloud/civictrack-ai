import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_roles
from app.models import User, UserRole
from app.routers.complaints import get_complaint_or_404
from app.schemas import ComplaintOut

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

router = APIRouter(prefix="/api/complaints", tags=["complaints"])


def detect_extension(data: bytes) -> str | None:
    """Checks the real file type from its first bytes."""
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return None


@router.post("/{complaint_id}/image", response_model=ComplaintOut)
def upload_image(
    complaint_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.citizen)),
):
    complaint = get_complaint_or_404(db, complaint_id)
    if complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to do this")

    data = file.file.read(MAX_SIZE + 1)
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Image must be 5 MB or smaller")

    extension = detect_extension(data)
    if extension is None:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG or WEBP images are allowed")

    UPLOAD_DIR.mkdir(exist_ok=True)
    filename = f"{uuid.uuid4().hex}{extension}"
    (UPLOAD_DIR / filename).write_bytes(data)

    complaint.image_path = f"/uploads/{filename}"
    db.commit()
    db.refresh(complaint)
    return complaint