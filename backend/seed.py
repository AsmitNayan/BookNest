"""Run this once to populate sample data: python seed.py"""
from database import SessionLocal, engine
import models, crud, schemas

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

books = [
    schemas.BookCreate(title="The Midnight Library", author="Matt Haig", genre="Fiction", isbn="9780525559474", published_year=2020, total_copies=3, description="A dazzling novel about all the choices that go into a life well lived."),
    schemas.BookCreate(title="Atomic Habits", author="James Clear", genre="Self-Help", isbn="9780735211292", published_year=2018, total_copies=4, description="Tiny changes, remarkable results."),
    schemas.BookCreate(title="Project Hail Mary", author="Andy Weir", genre="Sci-Fi", isbn="9780593135204", published_year=2021, total_copies=2, description="A lone astronaut must save the earth from disaster."),
    schemas.BookCreate(title="The Alchemist", author="Paulo Coelho", genre="Fiction", isbn="9780062315007", published_year=1988, total_copies=5, description="A magical story about following your dreams."),
    schemas.BookCreate(title="Educated", author="Tara Westover", genre="Memoir", isbn="9780399590504", published_year=2018, total_copies=2, description="A memoir about a young girl kept out of school."),
    schemas.BookCreate(title="Dune", author="Frank Herbert", genre="Sci-Fi", isbn="9780441013593", published_year=1965, total_copies=3, description="Epic science fiction set on the desert planet Arrakis."),
]

members = [
    schemas.MemberCreate(name="Aanya Sharma", email="aanya@example.com", phone="9876543210"),
    schemas.MemberCreate(name="Rohan Mehta", email="rohan@example.com", phone="9123456780"),
    schemas.MemberCreate(name="Priya Nair", email="priya@example.com", phone="9988776655"),
]

created_books = [crud.create_book(db, b) for b in books]
created_members = [crud.create_member(db, m) for m in members]

crud.create_lending(db, schemas.LendingCreate(book_id=created_books[0].id, member_id=created_members[0].id))
crud.create_lending(db, schemas.LendingCreate(book_id=created_books[2].id, member_id=created_members[1].id))

crud.create_review(db, created_books[0].id, schemas.ReviewCreate(member_id=created_members[0].id, rating=5, comment="Absolutely beautiful. Changed my perspective on life."))
crud.create_review(db, created_books[1].id, schemas.ReviewCreate(member_id=created_members[1].id, rating=4, comment="Super practical. Small habits really do add up!"))
crud.create_review(db, created_books[2].id, schemas.ReviewCreate(member_id=created_members[2].id, rating=5, comment="Best sci-fi I've read in years. Couldn't put it down."))

print("✅ Seed data inserted successfully!")
db.close()
