from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_profile
from app.models.profile import Profile
from app.models.document import Document

router = APIRouter(
  prefix="/documents",
  tags=["Documents"]
)


@router.get("/")
def get_documents(
  db: Session = Depends(get_db),
  current_profile: Profile = Depends(get_current_profile)
):
  documents = (
    db.query(Document)
    .filter(Document.user_id == current_profile.id)
    .order_by(Document.created_at.desc())
    .all()
  )

  return [
    {
        "id": str(document.id),
        "title": document.title,
        "file_name": document.file_name,
        "file_url": document.file_url,
        "file_type": document.file_type,
        "status": document.status,
        "created_at": document.created_at
    }
    for document in documents
  ]