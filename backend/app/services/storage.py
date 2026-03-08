import os
import uuid
from pathlib import Path

import aiofiles

from app.config import settings


def get_upload_path(filename: str) -> Path:
    return Path(settings.upload_dir) / filename


async def save_upload(file_bytes: bytes, original_filename: str) -> str:
    """Save uploaded file and return the relative URL path."""
    ext = Path(original_filename).suffix.lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    dest = get_upload_path(filename)

    os.makedirs(settings.upload_dir, exist_ok=True)

    async with aiofiles.open(dest, "wb") as f:
        await f.write(file_bytes)

    return f"/uploads/{filename}"


def delete_upload(photo_url: str) -> None:
    """Delete a photo file from disk given its URL path."""
    if not photo_url:
        return
    filename = photo_url.split("/uploads/")[-1]
    path = get_upload_path(filename)
    try:
        path.unlink(missing_ok=True)
    except Exception:
        pass
