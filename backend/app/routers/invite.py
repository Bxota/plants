from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.invitation import Invitation
from app.models.user import User

router = APIRouter(prefix="/api/invite", tags=["invite"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _get_valid_invitation(invitation: Invitation | None) -> Invitation:
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation introuvable")
    if invitation.used_at is not None:
        raise HTTPException(status_code=410, detail="Cette invitation a déjà été utilisée")
    if invitation.expires_at and invitation.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="Cette invitation a expiré")
    return invitation


@router.get("/{token}")
async def check_invitation(token: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invitation).where(Invitation.token == token))
    _get_valid_invitation(result.scalar_one_or_none())
    return {"valid": True}


class RegisterRequest(BaseModel):
    username: str
    password: str


@router.post("/{token}", status_code=status.HTTP_201_CREATED)
async def register_with_invitation(
    token: UUID,
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Invitation).where(Invitation.token == token))
    invitation = _get_valid_invitation(result.scalar_one_or_none())

    existing = await db.execute(select(User).where(User.username == data.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Ce nom d'utilisateur est déjà pris")

    user = User(
        username=data.username,
        password_hash=pwd_context.hash(data.password),
        is_admin=False,
    )
    db.add(user)
    await db.flush()  # pour obtenir user.id

    invitation.used_at = datetime.now(timezone.utc)
    invitation.used_by_id = user.id

    await db.commit()
    return {"message": "Compte créé avec succès"}
