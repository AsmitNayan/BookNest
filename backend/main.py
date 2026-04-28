from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BookNest API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Books ──────────────────────────────────────────────
@app.get("/books", response_model=List[schemas.Book])
def list_books(search: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_books(db, search)

@app.get("/books/{book_id}", response_model=schemas.BookDetail)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book

@app.post("/books", response_model=schemas.Book)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    if not crud.delete_book(db, book_id):
        raise HTTPException(404, "Book not found")
    return {"message": "Book deleted"}

# ── Members ────────────────────────────────────────────
@app.get("/members", response_model=List[schemas.Member])
def list_members(db: Session = Depends(get_db)):
    return crud.get_members(db)

@app.post("/members", response_model=schemas.Member)
def add_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    if crud.get_member_by_email(db, member.email):
        raise HTTPException(400, "Email already registered")
    return crud.create_member(db, member)

@app.get("/members/{member_id}", response_model=schemas.MemberDetail)
def get_member(member_id: int, db: Session = Depends(get_db)):
    m = crud.get_member(db, member_id)
    if not m:
        raise HTTPException(404, "Member not found")
    return m

# ── Lending ────────────────────────────────────────────
@app.get("/lendings", response_model=List[schemas.Lending])
def list_lendings(active_only: bool = False, db: Session = Depends(get_db)):
    return crud.get_lendings(db, active_only)

@app.post("/lendings", response_model=schemas.Lending)
def issue_book(lending: schemas.LendingCreate, db: Session = Depends(get_db)):
    book = crud.get_book(db, lending.book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    if book.available_copies < 1:
        raise HTTPException(400, "No copies available")
    if not crud.get_member(db, lending.member_id):
        raise HTTPException(404, "Member not found")
    return crud.create_lending(db, lending)

@app.patch("/lendings/{lending_id}/return", response_model=schemas.Lending)
def return_book(lending_id: int, db: Session = Depends(get_db)):
    lending = crud.return_book(db, lending_id)
    if not lending:
        raise HTTPException(404, "Lending record not found")
    return lending

# ── Reviews ────────────────────────────────────────────
@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    return crud.get_reviews(db, book_id)

@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
def add_review(book_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    if not crud.get_book(db, book_id):
        raise HTTPException(404, "Book not found")
    if not crud.get_member(db, review.member_id):
        raise HTTPException(404, "Member not found")
    return crud.create_review(db, book_id, review)

# ── Stats ──────────────────────────────────────────────
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)
