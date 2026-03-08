from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.plant import Plant
from app.models.user import User
from app.schemas.plant import PlantCreate, PlantResponse, PlantUpdate, ReorderItem

router = APIRouter(prefix="/api/plants", tags=["plants"])


def _own_or_404(plant: Plant | None, user: User) -> Plant:
    if not plant or plant.user_id != user.id:
        raise HTTPException(status_code=404, detail="Plante introuvable")
    return plant


@router.get("", response_model=list[PlantResponse])
async def list_plants(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Plant)
        .where(Plant.user_id == current_user.id)
        .order_by(Plant.sort_order, Plant.created_at)
    )
    return result.scalars().all()


@router.post("", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
async def create_plant(
    data: PlantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plant = Plant(**data.model_dump(), user_id=current_user.id)
    db.add(plant)
    await db.commit()
    await db.refresh(plant)
    return plant


@router.get("/{plant_id}", response_model=PlantResponse)
async def get_plant(
    plant_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _own_or_404(await db.get(Plant, plant_id), current_user)


@router.put("/{plant_id}", response_model=PlantResponse)
async def update_plant(
    plant_id: UUID,
    data: PlantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plant = _own_or_404(await db.get(Plant, plant_id), current_user)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(plant, field, value)

    await db.commit()
    await db.refresh(plant)
    return plant


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plant(
    plant_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.services.storage import delete_upload

    plant = _own_or_404(await db.get(Plant, plant_id), current_user)

    if plant.photo_url:
        delete_upload(plant.photo_url)

    await db.delete(plant)
    await db.commit()


@router.patch("/reorder", status_code=status.HTTP_204_NO_CONTENT)
async def reorder_plants(
    items: list[ReorderItem],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    for item in items:
        await db.execute(
            update(Plant)
            .where(Plant.id == item.id, Plant.user_id == current_user.id)
            .values(sort_order=item.sort_order)
        )
    await db.commit()
