import os
import tempfile
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.pdf_service import extract_pdf_pages
from app.services.chunk_service import create_chunks
from app.services.embedding_service import generate_embedding
from app.schemas.rag import AskRequest
from app.schemas.rag import AskRequest
from app.services.llm_service import generate_answer_with_ollama

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    tenant_id: UUID = Form(...),
    user_id: UUID = Form(...),
    title: str = Form(...),
    room_id: Optional[UUID] = Form(None),
    db: Session = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos PDF."
        )

    temp_path = None
    document = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        pages = extract_pdf_pages(temp_path)

        all_chunks = []

        for page in pages:
            page_text = page["text"]

            if not page_text or not page_text.strip():
                continue

            chunks = create_chunks(page_text)

            for chunk in chunks:
                if chunk.strip():
                    all_chunks.append({
                        "page": page["page"],
                        "content": chunk
                    })

        if len(all_chunks) == 0:
            raise HTTPException(
                status_code=400,
                detail="No se pudo extraer texto del PDF. Puede ser un PDF escaneado o vacío."
            )

        document = Document(
            tenant_id=tenant_id,
            user_id=user_id,
            room_id=room_id,
            title=title,
            file_name=file.filename,
            file_url=f"local://{file.filename}",
            file_type=file.content_type,
            status="processing"
        )

        db.add(document)
        db.flush()

        for index, chunk in enumerate(all_chunks):
            embedding = generate_embedding(chunk["content"])

            document_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                page_number=chunk["page"],
                content=chunk["content"],
                embedding=embedding
            )

            db.add(document_chunk)

        document.status = "ready"

        db.commit()
        db.refresh(document)

        return {
            "message": "Documento procesado correctamente",
            "document_id": str(document.id),
            "pages": len(pages),
            "chunks": len(all_chunks),
            "status": document.status
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        if document and document.id:
            try:
                document.status = "error"
                db.add(document)
                db.commit()
            except Exception:
                db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Error procesando el documento: {str(error)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/ask")
def ask_document(
    body: AskRequest,
    db: Session = Depends(get_db)
):
    question_embedding = generate_embedding(body.question)

    query = text("""
        SELECT
            dc.content,
            dc.page_number,
            dc.chunk_index,
            1 - (dc.embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM document_chunks dc
        INNER JOIN documents d
            ON d.id = dc.document_id
        WHERE dc.document_id = :document_id
        AND d.user_id = :user_id
        AND d.status = 'ready'
        ORDER BY dc.embedding <=> CAST(:embedding AS vector)
        LIMIT 5;
    """)

    embedding_str = "[" + ",".join(map(str, question_embedding)) + "]"

    results = db.execute(
        query,
        {
            "embedding": embedding_str,
            "document_id": str(body.document_id),
            "user_id": str(body.user_id)
        }
    ).mappings().all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No se encontró información relacionada con tu pregunta en este documento."
        )

    sources = []

    for row in results:
        sources.append({
            "page_number": row["page_number"],
            "chunk_index": row["chunk_index"],
            "content": row["content"],
            "similarity": float(row["similarity"])
        })

    context = "\n\n".join(
        [
            f"[Página {row['page_number']}]\n{row['content']}"
            for row in results
        ]
    )

    answer = generate_answer_with_ollama(
        question=body.question,
        context=context
    )

    return {
        "answer": answer,
        "sources": sources
    }