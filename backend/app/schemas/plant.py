from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PlantBase(BaseModel):
    common_name: str | None = None
    scientific_name: str | None = None
    emoji: str = "🌿"
    watering: str | None = None
    light: str | None = None
    temperature: str | None = None
    humidity: str | None = None
    fertilization: str | None = None
    notes: str | None = None
    tags: list[str] = []
    sort_order: int = 0


class PlantCreate(PlantBase):
    common_name: str


class PlantUpdate(PlantBase):
    pass


class PlantResponse(PlantBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    photo_url: str | None = None
    ai_identified: bool = False

    model_config = {"from_attributes": True}


class AiIdentifyResponse(BaseModel):
    common_name: str
    scientific_name: str | None = None
    emoji: str = "🌿"
    watering: str | None = None
    light: str | None = None
    temperature: str | None = None
    humidity: str | None = None
    fertilization: str | None = None
    notes: str | None = None
    tags: list[str] = []
    confidence: str = "medium"


class ReorderItem(BaseModel):
    id: UUID
    sort_order: int
