from typing import List, Optional
from repository import BookRepository, ReviewRepository
from models import Book, Review


class BookService:
    def __init__(self, book_repo: BookRepository, review_repo: ReviewRepository):
        self.book_repo = book_repo
        self.review_repo = review_repo


    def list_books_with_avg(self, q: Optional[str] = None):
        books = self.book_repo.list_books(q=q)
        result = []
        for b in books:
            avg = self.book_repo.average_rating_for(b.id)
            result.append((b, avg))
        return result


    def add_or_update_review(self, book_id: int, username: str, rating: int, text: str) -> Review:
        # basic check
        book = self.book_repo.get_book(book_id)
        if not book:
            raise ValueError("Book not found")
        return self.review_repo.upsert_review(book_id, username, rating, text)


    def get_reviews(self, book_id: int) -> List[Review]:
        book = self.book_repo.get_book(book_id)
        if not book:
            raise ValueError("Book not found")
        return self.review_repo.list_reviews(book_id)