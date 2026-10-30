from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.model.book import Book


class BookRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, book: Book) -> Book:
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_all(self) -> list[Book]:
        return list(self.session.scalars(select(Book).order_by(Book.id)).all())

    def get_by_id(self, book_id: int) -> Book | None:
        return self.session.get(Book, book_id)

    def search(self, title: str | None = None, author: str | None = None) -> list[Book]:
        filters = []
        if title:
            filters.append(Book.title.ilike(f"%{title}%"))
        if author:
            filters.append(Book.author.ilike(f"%{author}%"))
        if not filters:
            return []

        statement = select(Book).where(or_(*filters)).order_by(Book.id)
        return list(self.session.scalars(statement).all())

    def update(self, book: Book) -> Book:
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.session.delete(book)
        self.session.commit()

