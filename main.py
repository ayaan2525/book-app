import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from database import Base, SessionLocal, engine, get_db
from models import Book
from schemas import LoginRequest, TokenResponse, BookOut, ReviewIn, ReviewOut
from repository import BookRepository, ReviewRepository
from services import BookService
from auth import AuthService, USERS


app = FastAPI(title="Book Records – Simple App with FastAPI and SQLAlchemy")


auth_service = AuthService()


# init DB and seed books from json
Base.metadata.create_all(bind=engine)

def seed_books(db: Session):
    # if db already has books, skip
    if db.query(Book).first():
        return
    try:
        with open("seed_data.json", "r") as f:
            data = json.load(f)
            for item in data:
                b = Book(title=item["title"], author=item["author"], genre=item.get("genre", ""))
                db.add(b)
            db.commit()
    except FileNotFoundError:
        # seed a default book if file missing
        db.add_all([
            Book(title="Fallback Book", author="Unknown", genre="Misc"),
        ])
        db.commit()


# run seeding at startup
db = SessionLocal()
try:
    seed_books(db)
finally:
    db.close()


# Dependency factories

def get_book_repo(db: Session = Depends(get_db)):
    return BookRepository(db)

def get_review_repo(db: Session = Depends(get_db)):
    return ReviewRepository(db)

def get_book_service(
    book_repo: BookRepository = Depends(get_book_repo),
    review_repo: ReviewRepository = Depends(get_review_repo),
    ):
    return BookService(book_repo, review_repo)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")
    
# Login and Token generation
@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")
    token = auth_service.create_access_token(form_data.username)
    return TokenResponse(access_token=token)


# get books with average ratings
@app.get("/books", response_model=list[BookOut])
def list_books(q: str | None = None, svc: BookService = Depends(get_book_service), current_user: str = Depends(auth_service.get_current_user)):
    result = svc.list_books_with_avg(q=q)
    out = []
    for book, avg in result:
        out.append(BookOut(id=book.id, title=book.title, author=book.author, genre=book.genre, average_rating=avg))
    return out


# post or update a review
@app.post("/books/{book_id}/reviews", response_model=ReviewOut)
def add_or_update_review(book_id: int, payload: ReviewIn, svc: BookService = Depends(get_book_service), current_user: str = Depends(auth_service.get_current_user)):
    try:
        r = svc.add_or_update_review(book_id, current_user, payload.rating, payload.text or "")
        return ReviewOut(id=r.id, username=r.username, rating=r.rating, text=r.text)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")

# get reviews for a book with book_id
@app.get("/books/{book_id}/reviews", response_model=list[ReviewOut])
def get_reviews(book_id: int, svc: BookService = Depends(get_book_service), current_user: str = Depends(auth_service.get_current_user)):
    try:
        reviews = svc.get_reviews(book_id)
        return [ReviewOut(id=r.id, username=r.username, rating=r.rating, text=r.text) for r in reviews]
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")