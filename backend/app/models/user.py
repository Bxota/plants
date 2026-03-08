import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    username = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
