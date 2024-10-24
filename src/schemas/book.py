from typing import Optional
from pydantic import BaseModel, PositiveInt, Field


class Book(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    year: Optional[PositiveInt] = Field(default=None, gt=1800, lt=2025)
    isbn: str = Field()


class BookToPatch(Book):
    title: Optional[str] = Field(default=None, min_length=3)
    author: Optional[str] = Field(default=None, min_length=3)
    isbn: Optional[str] = Field(default=None)