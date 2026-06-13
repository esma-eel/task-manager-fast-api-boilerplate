from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await crud.get_tasks(db, current_user.id)


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await crud.create_task(db, data, current_user.id)


@router.get("/{id_task}", response_model=TaskOut)
async def get_task(
    id_task: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await crud.get_task(db, id_task, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{id_task}", response_model=TaskOut)
async def update_task(
    id_task: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await crud.get_task(db, id_task, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await crud.update_task(db, task, data)


@router.delete("/{id_task}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id_task: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await crud.get_task(db, id_task, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await crud.delete_task(db, task)
