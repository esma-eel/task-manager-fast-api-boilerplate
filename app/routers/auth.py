from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.dependencies import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.schemas import AccessToken, RefreshRequest, Token, UserCreate, UserOut
from jose import JWTError, jwt
from config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    if await crud.get_user_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await crud.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return await crud.create_user(db, data.username, data.email, data.password)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token, expires_at = create_refresh_token({"sub": str(user.id)})
    await crud.save_refresh_token(db, user.id, refresh_token, expires_at)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=AccessToken)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid refresh token")
    try:
        payload = jwt.decode(data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    rt = await crud.get_refresh_token(db, data.refresh_token)
    if not rt or rt.expires_at < datetime.now(timezone.utc):
        raise credentials_exception

    access_token = create_access_token({"sub": user_id})
    return AccessToken(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    await crud.delete_refresh_token(db, data.refresh_token)
