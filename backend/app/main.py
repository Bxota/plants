from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app.config import settings
from app.database import AsyncSessionLocal
from app.routers import auth, plants, photos, admin


async def seed_admin():
    """Crée l'admin initial si aucun utilisateur n'existe en base."""
    from app.models.user import User

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        if result.first() is not None:
            return  # Des users existent déjà

        admin_user = User(
            username=settings.admin_username,
            password_hash=settings.admin_password_hash,
            is_admin=True,
        )
        db.add(admin_user)
        await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_admin()
    yield


app = FastAPI(title="Plantes API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(photos.router)
app.include_router(admin.router)

app.mount("/uploads", StaticFiles(directory=settings.upload_dir, check_dir=False), name="uploads")


@app.get("/health")
async def health():
    return {"status": "ok"}
