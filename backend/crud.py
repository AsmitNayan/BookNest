from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import date
import models, schemas

# ── Books ──────────────────────────────────────────────
def get_books(db: Session, search: str = None):
    q = db.query(models.Book)
    if search:
        q = q.filter(or_(
            models.Book.title.ilike(f"%{search}%"),
            models.Book.author.ilike(f"%{search}%"),
            models.Book.genre.ilike(f"%{search}%"),
        ))
    return q.all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump(), available_copies=book.total_copies)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True

# ── Members ────────────────────────────────────────────
def get_members(db: Session):
    return db.query(models.Member).all()

def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()

def get_member_by_email(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()

def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# ── Lending ────────────────────────────────────────────
def get_lendings(db: Session, active_only: bool = False):
    q = db.query(models.Lending)
    if active_only:
        q = q.filter(models.Lending.returned_on == None)
    return q.all()

def create_lending(db: Session, lending: schemas.LendingCreate):
    db_lending = models.Lending(**lending.model_dump())
    book = get_book(db, lending.book_id)
    book.available_copies -= 1
    db.add(db_lending)
    db.commit()
    db.refresh(db_lending)
    return db_lending

def return_book(db: Session, lending_id: int):
    lending = db.query(models.Lending).filter(models.Lending.id == lending_id).first()
    if not lending or lending.returned_on:
        return None
    lending.returned_on = date.today()
    lending.book.available_copies += 1
    db.commit()
    db.refresh(lending)
    return lending

# ── Reviews ────────────────────────────────────────────
def get_reviews(db: Session, book_id: int):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()

def create_review(db: Session, book_id: int, review: schemas.ReviewCreate):
    db_review = models.Review(book_id=book_id, **review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# ── Stats ──────────────────────────────────────────────
def get_stats(db: Session):
    total_books   = db.query(func.count(models.Book.id)).scalar()
    total_members = db.query(func.count(models.Member.id)).scalar()
    active_loans  = db.query(func.count(models.Lending.id)).filter(models.Lending.returned_on == None).scalar()
    total_reviews = db.query(func.count(models.Review.id)).scalar()
    overdue       = db.query(func.count(models.Lending.id)).filter(
        models.Lending.returned_on == None,
        models.Lending.due_date < date.today()
    ).scalar()
    return {
        "total_books":   total_books,
        "total_members": total_members,
        "active_loans":  active_loans,
        "total_reviews": total_reviews,
        "overdue_loans": overdue,
    }
