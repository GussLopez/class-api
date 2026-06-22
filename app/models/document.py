from sqlalchemy import Column, String, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))

    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    room_id = Column(UUID(as_uuid=True), nullable=True)

    title = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_url = Column(Text, nullable=False)
    file_type = Column(String, nullable=True)

    status = Column(String, nullable=False, server_default=text("'processing'"))
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))