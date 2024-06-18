from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User


class PostOut(BaseModel):
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class Payload(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
