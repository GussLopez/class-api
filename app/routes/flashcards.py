from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_profile
from app.models.profile import Profile
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.study_session import StudySession
from app.schemas.flashcard import GenerateFlashcardsRequest
from app.services.llm_service import generate_flashcards_with_ollama


router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcards"]
)


@router.post("/generate")
def generate_flashcards(
    body: GenerateFlashcardsRequest,
    db: Session = Depends(get_db),
    current_profile: Profile = Depends(get_current_profile)
):
    document = (
        db.query(Document)
        .filter(
            Document.id == body.document_id,
            Document.user_id == current_profile.id,
            Document.status == "ready"
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado o todavía no está listo."
        )

    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document.id)
        .order_by(DocumentChunk.chunk_index.asc())
        .limit(20)
        .all()
    )

    if len(chunks) == 0:
        raise HTTPException(
            status_code=404,
            detail="El documento no tiene contenido procesado."
        )

    context = "\n\n".join(
        [
            f"[Página {chunk.page_number}]\n{chunk.content}"
            for chunk in chunks
        ]
    )

    try:
        flashcards = generate_flashcards_with_ollama(
            context=context,
            total=body.total
        )

        session = StudySession(
            user_id=current_profile.id,
            document_id=document.id,
            type="flashcards",
            content={
                "document_id": str(document.id),
                "document_title": document.title,
                "flashcards": flashcards
            }
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return {
            "session_id": str(session.id),
            "document_id": str(document.id),
            "flashcards": flashcards
        }

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error generando flashcards: {str(error)}"
        )