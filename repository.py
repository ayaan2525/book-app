from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models import Book, Review
from typing import List, Optional, Tuple


class BookRepository:
    def __init__(self, db: Session):
        self.db = db


    def list_books(self, q: Optional[str] = None) -> List[Book]:
        stmt = select(Book)
        if q:
            like = f"%{q}%"
            stmt = stmt.where((Book.title.ilike(like)) | (Book.author.ilike(like)))
        stmt = stmt.order_by(Book.title.asc())
        return list(self.db.scalars(stmt))


    def get_book(self, book_id: int) -> Optional[Book]:
        return self.db.get(Book, book_id)


    def average_rating_for(self, book_id: int) -> float:
        stmt = select(func.coalesce(func.avg(Review.rating), 0.0)).where(Review.book_id == book_id)
        avg = self.db.execute(stmt).scalar_one()
        # round to one decimal place
        return float(round(avg or 0.0, 1))


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db


    def upsert_review(self, book_id: int, username: str, rating: int, text: str) -> Review:
        # Check existing
        stmt = select(Review).where(Review.book_id == book_id, Review.username == username)
        existing = self.db.execute(stmt).scalar_one_or_none()
        if existing:
            existing.rating = rating
            existing.text = text
            self.db.add(existing)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        r = Review(book_id=book_id, username=username, rating=rating, text=text or "")
        self.db.add(r)
        self.db.commit()
        self.db.refresh(r)
        return r


    def list_reviews(self, book_id: int) -> List[Review]:
        stmt = select(Review).where(Review.book_id == book_id).order_by(Review.id.desc())
        return list(self.db.scalars(stmt))