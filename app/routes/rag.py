from fastapi import APIRouter

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

@router.get("/health")
def health():
    return {
        "status": "ok"
    }