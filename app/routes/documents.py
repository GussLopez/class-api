from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.auth import get_current_profile
from app.models.profile import Profile
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

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

@router.get("/{document_id}")
def get_document_by_id(
  document_id: UUID,
  db: Session = Depends(get_db),
  current_profile: Profile = Depends(get_current_profile)
):
  document = (
    db.query(Document)
    .filter(
      Document.id == document_id,
      Document.user_id == current_profile.id
    )
    .first()
  )

  if document is None:
    raise HTTPException(
      status_code=404,
      detail="Documento no encontrado."
    )

  stats = (
    db.query(
        func.count(DocumentChunk.id).label("chunks_count"),
        func.max(DocumentChunk.page_number).label("pages_count")
    )
    .filter(DocumentChunk.document_id == document.id)
    .first()
  )

  return {
    "id": str(document.id),
    "tenant_id": str(document.tenant_id),
    "user_id": str(document.user_id),
    "room_id": str(document.room_id) if document.room_id else None,
    "title": document.title,
    "file_name": document.file_name,
    "file_url": document.file_url,
    "file_type": document.file_type,
    "status": document.status,
    "created_at": document.created_at,
    "chunks_count": stats.chunks_count or 0,
    "pages_count": stats.pages_count or 0
  }