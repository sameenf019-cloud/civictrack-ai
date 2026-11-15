from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models import Complaint, ComplaintStatus, User, UserRole
from app.schemas import AssignRequest, ComplaintCreate, ComplaintOut, StatusUpdate

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

OFFICER_ALLOWED = {ComplaintStatus.in_progress, ComplaintStatus.resolved}


def get_complaint_or_404(db: Session, complaint_id: int) -> Complaint:
    complaint = db.get(Complaint, complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


def can_view(user: User, complaint: Complaint) -> bool:
    if user.role == UserRole.admin:
        return True
    if user.role == UserRole.citizen:
        return complaint.citizen_id == user.id
    return complaint.officer_id == user.id


@router.post("", response_model=ComplaintOut, status_code=status.HTTP_201_CREATED)
def create_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.citizen)),
):
    complaint = Complaint(**payload.model_dump(), citizen_id=current_user.id)
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.get("", response_model=list[ComplaintOut])
def list_complaints(
    status_filter: ComplaintStatus | None = Query(default=None, alias="status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Complaint)
    if current_user.role == UserRole.citizen:
        query = query.filter(Complaint.citizen_id == current_user.id)
    elif current_user.role == UserRole.officer:
        query = query.filter(Complaint.officer_id == current_user.id)
    if status_filter is not None:
        query = query.filter(Complaint.status == status_filter)
    return query.order_by(Complaint.id.desc()).offset(skip).limit(limit).all()


@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    complaint = get_complaint_or_404(db, complaint_id)
    if not can_view(current_user, complaint):
        raise HTTPException(status_code=403, detail="You do not have permission to do this")
    return complaint


@router.patch("/{complaint_id}/assign", response_model=ComplaintOut)
def assign_complaint(
    complaint_id: int,
    payload: AssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
):
    complaint = get_complaint_or_404(db, complaint_id)
    officer = db.get(User, payload.officer_id)
    if officer is None or officer.role != UserRole.officer or not officer.is_active:
        raise HTTPException(status_code=400, detail="Invalid officer")
    complaint.officer_id = officer.id
    complaint.status = ComplaintStatus.assigned
    db.commit()
    db.refresh(complaint)
    return complaint


@router.patch("/{complaint_id}/status", response_model=ComplaintOut)
def update_status(
    complaint_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.officer)),
):
    complaint = get_complaint_or_404(db, complaint_id)
    if current_user.role == UserRole.officer:
        if complaint.officer_id != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to do this")
        if payload.status not in OFFICER_ALLOWED:
            raise HTTPException(status_code=403, detail="Officers can only set in_progress or resolved")
    complaint.status = payload.status
    db.commit()
    db.refresh(complaint)
    return complaint