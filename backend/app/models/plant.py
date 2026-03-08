import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.sql import func

from app.database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    common_name = Column(Text, nullable=False)
    scientific_name = Column(Text, nullable=True)
    emoji = Column(String(10), default="🌿")

    photo_url = Column(Text, nullable=True)

    watering = Column(Text, nullable=True)
    light = Column(Text, nullable=True)
    temperature = Column(Text, nullable=True)
    humidity = Column(Text, nullable=True)
    fertilization = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)
    tags = Column(ARRAY(Text), default=list)

    sort_order = Column(Integer, default=0)

    ai_identified = Column(Boolean, default=False)
    ai_raw_response = Column(JSONB, nullable=True)
