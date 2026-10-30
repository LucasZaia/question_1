from sqlalchemy.orm import Session

from app.model.book import Book, BookCreate, BookUpdate
from app.repository.book_repository import BookRepository


class BookNotFoundError(Exception):
    pass


class BookService:
    def __init__(self, session: Session) -> None:
        self.repository = BookRepository(session)

    def create(self, book_data: BookCreate) -> Book:
        book = Book(**book_data.model_dump())
        return self.repository.create(book)

    def list_all(self) -> list[Book]:
        return self.repository.get_all()

    def get_by_id(self, book_id: int) -> Book:
        book = self.repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundError(f"Book {book_id} was not found")
        return book

    def search(self, title: str | None = None, author: str | None = None) -> list[Book]:
        return self.repository.search(title=title, author=author)

    def update(self, book_id: int, book_data: BookUpdate) -> Book:
        book = self.get_by_id(book_id)
        for field, value in book_data.model_dump().items():
            setattr(book, field, value)
        return self.repository.update(book)

    def delete(self, book_id: int) -> None:
        book = self.get_by_id(book_id)
        self.repository.delete(book)

