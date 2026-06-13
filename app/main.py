from fastapi import FastAPI
from app.routers import auth, tasks
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} is running"}
