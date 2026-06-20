from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DocumentChunk(Base):
  __tablename__ = "document_chunks"

  id = Column(UUID(as_uuid=True), primary_key=True)

  document_id = Column(UUID(as_uuid=True))

  chunk_index = Column(Integer)

  page_number = Column(Integer)

  content = Column(Text)

  embedding = Column(Vector(1536))