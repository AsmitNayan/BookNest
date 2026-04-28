from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, timedelta

class Book(Base):
    __tablename__ = "books"

    id              = Column(Integer, primary_key=True, index=True)
    title           = Column(String(255), nullable=False)
    author          = Column(String(255), nullable=False)
    genre           = Column(String(100))
    isbn            = Column(String(20), unique=True)
    published_year  = Column(Integer)
    total_copies    = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    description     = Column(Text)

    lendings = relationship("Lending", back_populates="book")
    reviews  = relationship("Review",  back_populates="book")


class Member(Base):
    __tablename__ = "members"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(255), nullable=False)
    email      = Column(String(255), unique=True, nullable=False)
    phone      = Column(String(20))
    joined_on  = Column(Date, default=date.today)

    lendings = relationship("Lending", back_populates="member")
    reviews  = relationship("Review",  back_populates="member")


class Lending(Base):
    __tablename__ = "lendings"

    id          = Column(Integer, primary_key=True, index=True)
    book_id     = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id   = Column(Integer, ForeignKey("members.id"), nullable=False)
    issued_on   = Column(Date, default=date.today)
    due_date    = Column(Date, default=lambda: date.today() + timedelta(days=14))
    returned_on = Column(Date, nullable=True)

    book   = relationship("Book",   back_populates="lendings")
    member = relationship("Member", back_populates="lendings")


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("rating >= 1 AND rating <= 5"),)

    id        = Column(Integer, primary_key=True, index=True)
    book_id   = Column(Integer, ForeignKey("books.id"),   nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    rating    = Column(Integer, nullable=False)
    comment   = Column(Text)
    reviewed_on = Column(Date, default=date.today)

    book   = relationship("Book",   back_populates="reviews")
    member = relationship("Member", back_populates="reviews")
