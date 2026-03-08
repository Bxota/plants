import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.plant import Plant
from app.schemas.plant import AiIdentifyResponse
from app.services.ai import identify_plant
from app.services.storage import save_upload, delete_upload
from app.config import settings

router = APIRouter(tags=["photos"])
logger = logging.getLogger(__name__)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}


def _validate_upload(file: UploadFile, file_bytes: bytes) -> None:
    if file.content_type and file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Format non supporté (JPEG, PNG, WEBP)")
    if len(file_bytes) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux (max 10 Mo)")


@router.post("/api/identify", response_model=AiIdentifyResponse)
async def identify(
    photo: UploadFile = File(...),
    _: str = Depends(get_current_user),
):
    """Upload a photo and get AI-identified plant info without saving anything."""
    file_bytes = await photo.read()
    _validate_upload(photo, file_bytes)

    try:
        data = await identify_plant(file_bytes, photo.content_type or "image/jpeg")
    except json.JSONDecodeError as e:
        logger.error(f"Claude JSON parse error: {e}")
        # Return empty response so frontend can open a blank form
        return AiIdentifyResponse(
            common_name="Plante inconnue",
            confidence="low",
        )
    except Exception as e:
        logger.error(f"AI identification error: {e}")
        raise HTTPException(status_code=502, detail="Service d'identification indisponible")

    # Remove internal key before returning
    data.pop("ai_raw_response", None)
    return AiIdentifyResponse(**{k: v for k, v in data.items() if k in AiIdentifyResponse.model_fields})


@router.post("/api/plants/{plant_id}/photo", response_model=dict)
async def upload_photo(
    plant_id: UUID,
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: str = Depends(get_current_user),
):
    """Upload and attach a photo to an existing plant."""
    plant = await db.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plante introuvable")

    file_bytes = await photo.read()
    _validate_upload(photo, file_bytes)

    # Delete old photo if any
    if plant.photo_url:
        delete_upload(plant.photo_url)

    photo_url = await save_upload(file_bytes, photo.filename or "photo.jpg")
    plant.photo_url = photo_url

    await db.commit()
    return {"photo_url": photo_url}
