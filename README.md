# 📚 BookNest — Book Lending & Reading Community
### DBMS Project | FastAPI + PostgreSQL

---

## Project Structure

```
booknest/
├── backend/
│   ├── main.py          # FastAPI app + all routes
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # PostgreSQL connection
│   ├── seed.py          # Sample data
│   └── requirements.txt
└── frontend/
    └── index.html       # Full UI (single file)
```

---

## Database Schema

- **books** — title, author, genre, isbn, published_year, total_copies, available_copies, description
- **members** — name, email, phone, joined_on
- **lendings** — book_id, member_id, issued_on, due_date, returned_on
- **reviews** — book_id, member_id, rating (1–5), comment, reviewed_on

---

## Setup

### 1. PostgreSQL
```bash
# Create database
psql -U postgres
CREATE DATABASE booknest;
\q
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt

# Set DB URL (optional, defaults to localhost)
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/booknest"

# Run server
uvicorn main:app --reload
```

### 3. Seed sample data
```bash
python seed.py
```

### 4. Frontend
Just open `frontend/index.html` in your browser.
> Make sure backend is running on `http://localhost:8000`

---

## Features

| Feature | Description |
|---|---|
| 📚 Books | Add, browse, search, delete books |
| 👥 Members | Register and view community members |
| 🔄 Lending | Issue books, return them, track overdue |
| ⭐ Reviews | Rate and review books (1–5 stars) |
| 📊 Dashboard | Live stats — books, members, loans, overdue |

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | /books | List all books (with search) |
| POST | /books | Add a new book |
| DELETE | /books/{id} | Delete a book |
| GET | /members | List all members |
| POST | /members | Add a member |
| GET | /lendings | List lendings |
| POST | /lendings | Issue a book |
| PATCH | /lendings/{id}/return | Return a book |
| GET | /books/{id}/reviews | Get reviews for a book |
| POST | /books/{id}/reviews | Add a review |
| GET | /stats | Dashboard statistics |

API Docs: http://localhost:8000/docs
