import asyncio
import random
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.models import Base, User, Task
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SAMPLE_TASKS = [
    "Design database schema",
    "Implement authentication",
    "Write unit tests",
    "Setup CI/CD pipeline",
    "Code review",
    "Fix login bug",
    "Add pagination",
    "Update documentation",
    "Optimize queries",
    "Deploy to staging",
    "Security audit",
    "Refactor auth module",
    "Add email verification",
    "Setup monitoring",
    "Write API docs",
    "Performance testing",
    "Fix CORS issue",
    "Add rate limiting",
    "Migrate database",
    "Implement caching",
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Create 10 users
        users = []
        for i in range(1, 11):
            user = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
                hashed_password=pwd_context.hash(f"password{i}"),
                is_active=True,
                created_at=datetime.now(timezone.utc),
            )
            session.add(user)
            users.append(user)

        await session.flush()  # get IDs before creating tasks

        # Create 200 tasks
        titles = (SAMPLE_TASKS * 10)[:200]
        for i, title in enumerate(titles, start=1):
            task = Task(
                title=f"{title} #{i}",
                description=f"Description for task {i}",
                is_completed=random.choice([True, False]),
                created_at=datetime.now(timezone.utc),
                owner_id=random.choice(users).id,
            )
            session.add(task)

        await session.commit()
        print("Seed complete: 10 users and 200 tasks inserted.")


if __name__ == "__main__":
    asyncio.run(seed())
