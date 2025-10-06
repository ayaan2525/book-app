from pydantic import BaseModel, Field
from typing import Optional, List


# Auth
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Books
class BookBase(BaseModel):
    title: str
    author: str
    genre: str


class BookOut(BookBase):
    id: int
    average_rating: float = 0.0


# Reviews
class ReviewIn(BaseModel):
    rating: int = Field(ge=1, le=5)
    text: Optional[str] = ""


class ReviewOut(BaseModel):
    id: int
    username: str
    rating: int
    text: str