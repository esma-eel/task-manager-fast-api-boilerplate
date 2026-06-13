from datetime import datetime
from pydantic import BaseModel, EmailStr


# User
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# Auth
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Task
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    owner_id: int

    model_config = {"from_attributes": True}
