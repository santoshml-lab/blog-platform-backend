from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


# =========================
# AUTH SCHEMAS
# =========================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


# =========================
# POST SCHEMAS
# =========================

class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# COMMENT SCHEMAS
# =========================

class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
