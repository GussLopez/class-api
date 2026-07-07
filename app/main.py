from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import documents
from app.routes import rag
from app.routes import flashcards

app = FastAPI(
  title="Study AI API",
  version="1.0.0"
)

origins = [
  "http://localhost:3000",
  "http://127.0.0.1:3000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(rag.router)
app.include_router(flashcards.router)