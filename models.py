from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, UniqueConstraint
from database import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=False, index=True)


    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), index=True)
    username: Mapped[str] = mapped_column(String(100), index=True) # who wrote it
    rating: Mapped[int] = mapped_column(Integer) # 1..5
    text: Mapped[str] = mapped_column(Text, default="")


    book = relationship("Book", back_populates="reviews")


    __table_args__ = (
    UniqueConstraint("book_id", "username", name="uq_review_per_user_per_book"),
    )