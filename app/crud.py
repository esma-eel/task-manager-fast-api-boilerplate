from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task, User, RefreshToken
from app.schemas import TaskCreate, TaskUpdate
from app.dependencies import hash_password


# User
async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# Refresh Token
async def save_refresh_token(db: AsyncSession, user_id: int, token: str, expires_at) -> None:
    rt = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(rt)
    await db.commit()

async def get_refresh_token(db: AsyncSession, token: str) -> RefreshToken | None:
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    return result.scalar_one_or_none()

async def delete_refresh_token(db: AsyncSession, token: str) -> None:
    rt = await get_refresh_token(db, token)
    if rt:
        await db.delete(rt)
        await db.commit()


# Task
async def get_tasks(db: AsyncSession, owner_id: int) -> list[Task]:
    result = await db.execute(select(Task).where(Task.owner_id == owner_id))
    return list(result.scalars().all())

async def get_task(db: AsyncSession, task_id: int, owner_id: int) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    )
    return result.scalar_one_or_none()

async def create_task(db: AsyncSession, data: TaskCreate, owner_id: int) -> Task:
    task = Task(**data.model_dump(), owner_id=owner_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def update_task(db: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()
