from fastapi import FastAPI

from app.routes import documents
from app.routes import rag

app = FastAPI(
  title="Study AI API",
  version="1.0.0"
)

app.include_router(documents.router)
app.include_router(rag.router)