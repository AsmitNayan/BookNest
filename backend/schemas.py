from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# ── Book ───────────────────────────────────────────────
class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int = 1
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available_copies: int

    class Config:
        from_attributes = True

class BookDetail(Book):
    reviews: List["Review"] = []

# ── Member ─────────────────────────────────────────────
class MemberBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    joined_on: date

    class Config:
        from_attributes = True

class MemberDetail(Member):
    lendings: List["Lending"] = []

# ── Lending ────────────────────────────────────────────
class LendingCreate(BaseModel):
    book_id: int
    member_id: int

class Lending(BaseModel):
    id: int
    book_id: int
    member_id: int
    issued_on: date
    due_date: date
    returned_on: Optional[date] = None
    book: Optional[Book] = None
    member: Optional[Member] = None

    class Config:
        from_attributes = True

# ── Review ─────────────────────────────────────────────
class ReviewCreate(BaseModel):
    member_id: int
    rating: int
    comment: Optional[str] = None

class Review(BaseModel):
    id: int
    book_id: int
    member_id: int
    rating: int
    comment: Optional[str] = None
    reviewed_on: date
    member: Optional[Member] = None

    class Config:
        from_attributes = True

BookDetail.model_rebuild()
MemberDetail.model_rebuild()
