from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
import tempfile

from app.services.pdf_service import extract_pdf_pages
from app.services.chunk_service import create_chunks

from app.services.embedding_service import generate_embedding

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
    db: Session = Depends(get_db)
):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        content = await file.read()

        temp_file.write(content)

        pdf_path = temp_file.name

    pages = extract_pdf_pages(pdf_path)

    all_chunks = []

    for page in pages:

        chunks = create_chunks(
            page["text"]
        )

        for chunk in chunks:
            all_chunks.append({
                "page": page["page"],
                "content": chunk
            })

    first_chunk = all_chunks[0]["content"]

    embedding = generate_embedding(first_chunk)

    return {
        "pages": len(pages),
        "chunks": len(all_chunks),
        "embedding_dimensions": len(embedding)
    }