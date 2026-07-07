from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.models.base import Base


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    user_id = Column(UUID(as_uuid=True), nullable=False)
    document_id = Column(UUID(as_uuid=True), nullable=True)

    type = Column(String, nullable=False)
    content = Column(JSONB, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("now()")
    )