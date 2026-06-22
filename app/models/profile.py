from sqlalchemy import Column, String, Text, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base


class Profile(Base):
  __tablename__ = "profiles"

  id = Column(UUID(as_uuid=True), primary_key=True)
  tenant_id = Column(UUID(as_uuid=True), nullable=False)

  name = Column(String, nullable=False)
  last_name = Column(Text, nullable=True)
  email = Column(Text, nullable=True)

  avatar_url = Column(Text, nullable=True)
  role = Column(String, nullable=True)

  sex = Column(Text, nullable=True)
  age = Column(SmallInteger, nullable=True)