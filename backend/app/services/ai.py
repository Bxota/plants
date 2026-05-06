import asyncio
import json
import logging

from google import genai
from google.genai import types
from PIL import Image
import io

from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Tu es un botaniste expert. À partir d'une photo de plante,
tu identifies l'espèce et fournis des conseils de soin précis et fiables.
Tu réponds UNIQUEMENT avec un objet JSON valide, sans markdown, sans texte
autour. Si tu ne peux pas identifier la plante avec certitude, tu fournis quand
même des valeurs plausibles et tu indiques confidence: "low"."""

USER_PROMPT = """Identifie cette plante et retourne EXACTEMENT ce JSON (aucun texte avant ou après) :

{
  "common_name": "Nom commun en français",
  "scientific_name": "Genre espèce",
  "emoji": "emoji parmi 🌿🌱🌵🌴🌺🌸🌼🍃🎋🪴",
  "watering": "Fréquence et méthode d'arrosage, 1-2 phrases",
  "light": "Besoins en lumière, 1 phrase",
  "temperature": "Plage de température idéale, ex: 18 – 25 °C",
  "humidity": "Besoins en humidité, 1 phrase",
  "fertilization": "Rythme de fertilisation ou null si non pertinent",
  "levels": {
    "water": 3,
    "light": 4,
    "temp": 2,
    "humidity": 4,
    "fertilizer": 2
  },
  "notes": "Note de soin importante ou particularité botanique, 1-2 phrases",
  "tags": ["tag1", "tag2", "tag3"],
  "confidence": "high"
}

Pour levels, utilise une échelle 1-5 (1 = besoin minimal, 5 = besoin maximal) :
- water : fréquence d'arrosage (1=rarement, 5=très souvent)
- light : intensité lumineuse requise (1=ombre, 5=plein soleil)
- temp : préférence de chaleur (1=frais <15°C, 5=chaud >25°C)
- humidity : humidité ambiante requise (1=air sec, 5=très humide)
- fertilizer : besoin en engrais (1=jamais, 5=très fréquent)

Pour les tags, utilise des termes comme : Tropical, Mi-ombre, Plein soleil, Humidité haute,
Feuillage décoratif, Floraison, Architectural, Succulente, Cactus, Feuillage persistant,
Grandes feuilles, Peut fleurir. Maximum 4 tags."""


def _resize_image(image_bytes: bytes, max_dimension: int = 1600) -> bytes:
    """Resize image if too large and return as JPEG bytes."""
    img = Image.open(io.BytesIO(image_bytes))

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    width, height = img.size
    if max(width, height) > max_dimension:
        ratio = max_dimension / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=85, optimize=True)
    return output.getvalue()


MODELS_FALLBACK = ["gemini-2.5-flash", "gemini-3-flash"]


def _call_model_sync(client: genai.Client, model: str, image_part: types.Part) -> str:
    response = client.models.generate_content(
        model=model,
        contents=[USER_PROMPT, image_part],
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text


async def identify_plant(image_bytes: bytes, media_type: str) -> dict:
    """Call Gemini Vision to identify a plant and return structured care info."""
    try:
        resized_bytes = _resize_image(image_bytes)
    except Exception as e:
        logger.warning(f"Image resize failed, using original: {e}")
        resized_bytes = image_bytes

    client = genai.Client(api_key=settings.gemini_api_key)
    image_part = types.Part.from_bytes(data=resized_bytes, mime_type="image/jpeg")

    last_error: Exception | None = None
    used_model = MODELS_FALLBACK[0]
    raw_text: str | None = None
    for model in MODELS_FALLBACK:
        for attempt in range(2):
            try:
                raw_text = await asyncio.to_thread(
                    _call_model_sync, client, model, image_part
                )
                used_model = model
                logger.info(
                    f"Gemini response via {model} (attempt {attempt + 1}): {raw_text[:200]}"
                )
                break
            except Exception as e:
                last_error = e
                logger.warning(f"Model {model} attempt {attempt + 1} failed: {e}")
                if attempt == 0:
                    await asyncio.sleep(1)
        else:
            continue
        break
    else:
        raise last_error

    logger.info(f"Gemini raw response ({used_model}): {raw_text[:200]}")

    # Defensive JSON parse — strip any accidental markdown fences
    clean = raw_text.strip()
    if clean.startswith("```"):
        clean = clean.split("```")[1]
        if clean.startswith("json"):
            clean = clean[4:]
        clean = clean.strip()

    data = json.loads(clean)

    # Ensure required fields exist
    for field in ["common_name", "watering", "light", "temperature", "tags"]:
        if field not in data:
            data[field] = None if field != "tags" else []

    # Validate levels structure ; reset to None if malformed so front can fallback
    lvl = data.get("levels")
    if not isinstance(lvl, dict) or not all(
        k in lvl for k in ("water", "light", "temp", "humidity", "fertilizer")
    ):
        data["levels"] = None
    else:
        data["levels"] = {
            k: max(1, min(5, int(lvl[k])))
            for k in ("water", "light", "temp", "humidity", "fertilizer")
        }

    data["ai_raw_response"] = {"model": used_model, "raw": raw_text}
    return data
