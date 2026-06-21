from uuid import UUID
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    document_id: UUID
    user_id: UUID
    question: str = Field(
        min_length=3,
        max_length=1000
    )


class SourceChunk(BaseModel):
    page_number: int | None
    chunk_index: int
    content: str
    similarity: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]