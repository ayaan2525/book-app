import unittest
from unittest.mock import Mock, MagicMock
import pytest

# Mocking the models before importing the services
mock_models = MagicMock()
# mock the classes that are used in type hints in the service
mock_models.Book = MagicMock()
mock_models.Review = MagicMock()

import sys
sys.modules['models'] = mock_models

from services import BookService
from models import Book, Review

class BookServiceTest(unittest.TestCase):

    def setUp(self):
        """Set up mock repositories for each test."""
        # Ensure that calls to the mocked Book and Review classes return a
        # NEW mock object for each call. This prevents state from being
        # shared across mock instances within and between tests.
        Book.side_effect = lambda **kwargs: MagicMock(**kwargs)
        Review.side_effect = lambda **kwargs: MagicMock(**kwargs)

        self.mock_book_repo = Mock()
        self.mock_review_repo = Mock()
        self.book_service = BookService(self.mock_book_repo, self.mock_review_repo)

    def test_list_books_with_avg(self):
        """
        Test that list_books_with_avg returns a list of books with their calculated average ratings.
        """

        # Set up the mock data the repositories will return
        mock_books = [
            Book(id=1, title="Test Book 1", author="Author A", genre="Literature"),
            Book(id=2, title="Test Book 2", author="Author B", genre="Science"),
        ]
        self.mock_book_repo.list_books.return_value = mock_books
        self.mock_book_repo.average_rating_for.side_effect = [4.5, 3.0]

        # Call the service method
        result = self.book_service.list_books_with_avg(q=None)

        # Check that the service method returned the expected data structure and values
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (mock_books[0], 4.5))
        self.assertEqual(result[1], (mock_books[1], 3.0))
        self.mock_book_repo.list_books.assert_called_once_with(q=None)
        self.mock_book_repo.average_rating_for.assert_any_call(1)
        self.mock_book_repo.average_rating_for.assert_any_call(2)

    def test_add_or_update_review_book_exists(self):
        """
        Test adding a review for a book that exists.
        """
        # set up the mock data
        book_id = 1
        username = "testuser"
        rating = 5
        text = "Great book!"
        mock_book = Book(id=book_id, title="Existing Book", author="Author", genre="Genre")
        mock_review = Review(id=1, book_id=book_id, username=username, rating=rating, text=text)

        self.mock_book_repo.get_book.return_value = mock_book
        self.mock_review_repo.upsert_review.return_value = mock_review

        # call the service method
        result = self.book_service.add_or_update_review(book_id, username, rating, text)

        # check the result and that the mocks were called as expected
        self.assertEqual(result, mock_review)
        self.mock_book_repo.get_book.assert_called_once_with(book_id)
        self.mock_review_repo.upsert_review.assert_called_once_with(book_id, username, rating, text)

    def test_add_or_update_review_book_not_found_raises_error(self):
        """
        Test that adding a review for a non-existent book raises a ValueError.
        """
        # set up the mock to simulate book not found
        book_id = 999  # An ID that doesn't exist
        self.mock_book_repo.get_book.return_value = None

        # call the service method and assert it raises ValueError
        with pytest.raises(ValueError, match="Book not found"):
            self.book_service.add_or_update_review(book_id, "testuser", 5, "text")

        self.mock_book_repo.get_book.assert_called_once_with(book_id)
        self.mock_review_repo.upsert_review.assert_not_called()

    def test_get_reviews_for_book(self):
        """
        Test fetching all reviews for a specific book.
        """
        # set up the mock data
        book_id = 1
        mock_book = Book(id=book_id, title="A Book With Reviews", author="Author", genre="Genre")
        mock_reviews = [
            Review(id=1, book_id=book_id, username="user1", rating=5, text="Loved it!"),
            Review(id=2, book_id=book_id, username="user2", rating=4, text="Pretty good."),
        ]
        self.mock_book_repo.get_book.return_value = mock_book
        self.mock_review_repo.list_reviews.return_value = mock_reviews

        # call the service method
        reviews = self.book_service.get_reviews(book_id)

        # check the result and that the mocks were called as expected
        self.assertEqual(reviews, mock_reviews)
        self.mock_book_repo.get_book.assert_called_once_with(book_id)
        self.mock_review_repo.list_reviews.assert_called_once_with(book_id)

if __name__ == '__main__':
    unittest.main()

