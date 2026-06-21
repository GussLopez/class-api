from sqlalchemy import Column, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from app.models.base import Base

class DocumentChunk(Base):
  __tablename__ = "document_chunks"

  id = Column(
      UUID(as_uuid=True),
      primary_key=True,
      server_default=text("gen_random_uuid()")
  )

  document_id = Column(UUID(as_uuid=True), nullable=False)
  chunk_index = Column(Integer, nullable=False)
  page_number = Column(Integer, nullable=True)
  content = Column(Text, nullable=False)
  embedding = Column(Vector(384), nullable=True)