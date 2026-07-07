from uuid import UUID
from pydantic import BaseModel, Field


class GenerateFlashcardsRequest(BaseModel):
    document_id: UUID
    total: int = Field(default=10, ge=3, le=20)


class FlashcardItem(BaseModel):
    question: str = Field(min_length=3)
    answer: str = Field(min_length=3)


class GenerateFlashcardsResponse(BaseModel):
    session_id: str
    document_id: str
    flashcards: list[FlashcardItem]