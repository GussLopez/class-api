from uuid import UUID
from pydantic import BaseModel, Field


class GenerateFlashcardsRequest(BaseModel):
    document_id: UUID
    total: int = Field(default=6, ge=3, le=12)


class InfographicCard(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=10)
    points: list[str] = Field(min_length=2)


class GenerateFlashcardsResponse(BaseModel):
    session_id: str
    document_id: str
    cards: list[InfographicCard]