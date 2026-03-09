import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, text

from app.config import settings
from app.database import AsyncSessionLocal
from app.routers import auth, plants, photos, admin, invite

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent.parent / "migrations"


async def run_migrations():
    """Applique les fichiers .sql du dossier migrations/ qui n'ont pas encore été joués."""
    async with AsyncSessionLocal() as db:
        await db.execute(text("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
        """))
        await db.commit()

        applied = {row[0] for row in (await db.execute(text("SELECT filename FROM schema_migrations"))).fetchall()}

        for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if sql_file.name in applied:
                continue
            logger.info("Migration : %s", sql_file.name)
            for statement in sql_file.read_text().split(";"):
                statement = statement.strip()
                if statement:
                    await db.execute(text(statement))
            await db.execute(text("INSERT INTO schema_migrations (filename) VALUES (:f)"), {"f": sql_file.name})
            await db.commit()


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
    await run_migrations()
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
app.include_router(invite.router)

app.mount("/uploads", StaticFiles(directory=settings.upload_dir, check_dir=False), name="uploads")


@app.get("/health")
async def health():
    return {"status": "ok"}
