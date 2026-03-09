from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_admin_user
from app.models.invitation import Invitation
from app.models.user import User
from app.services.email import send_invitation_email

router = APIRouter(prefix="/api/admin", tags=["admin"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserResponse(BaseModel):
    id: UUID
    username: str
    is_admin: bool

    model_config = {"from_attributes": True}


class CreateUserRequest(BaseModel):
    username: str
    password: str
    is_admin: bool = False


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    result = await db.execute(select(User).order_by(User.created_at))
    return result.scalars().all()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    existing = await db.execute(select(User).where(User.username == data.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Ce nom d'utilisateur est déjà pris")

    user = User(
        username=data.username,
        password_hash=pwd_context.hash(data.password),
        is_admin=data.is_admin,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_admin_user),
):
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas supprimer votre propre compte")

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    await db.delete(user)
    await db.commit()


# ── Invitations ────────────────────────────────────────────────────────────────


class InvitationResponse(BaseModel):
    id: UUID
    token: UUID
    created_at: datetime
    expires_at: datetime | None
    used_at: datetime | None
    invited_email: str | None

    model_config = {"from_attributes": True}


class CreateInvitationRequest(BaseModel):
    email: str | None = None


@router.get("/invitations", response_model=list[InvitationResponse])
async def list_invitations(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    result = await db.execute(select(Invitation).order_by(Invitation.created_at.desc()))
    return result.scalars().all()


@router.post("/invitations", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
async def create_invitation(
    data: CreateInvitationRequest,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_admin_user),
):
    invitation = Invitation(
        created_by_id=current_admin.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        invited_email=data.email or None,
    )
    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)

    if data.email:
        await send_invitation_email(data.email, str(invitation.token))

    return invitation


@router.delete("/invitations/{token}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_invitation(
    token: UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    result = await db.execute(select(Invitation).where(Invitation.token == token))
    invitation = result.scalar_one_or_none()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation introuvable")
    await db.delete(invitation)
    await db.commit()
