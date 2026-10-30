from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.model.book import Book
from app.repository.book_repository import BookRepository


@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as database_session:
        yield database_session


def make_book(title: str) -> Book:
    return Book(
        title=title,
        author="J. R. R. Tolkien",
        publication_date=date(1937, 9, 21),
        summary="A hobbit goes on an unexpected journey.",
    )


def test_repository_creates_and_gets_a_book(session: Session) -> None:
    repository = BookRepository(session)

    created = repository.create(make_book("The Hobbit"))

    assert created.id is not None
    assert repository.get_by_id(created.id).title == "The Hobbit"


def test_repository_returns_none_for_an_unknown_id(session: Session) -> None:
    repository = BookRepository(session)

    assert repository.get_by_id(999) is None


def test_repository_lists_books_in_id_order(session: Session) -> None:
    repository = BookRepository(session)
    repository.create(make_book("The Lord of the Rings"))
    repository.create(make_book("The Hobbit"))

    books = repository.get_all()

    assert [book.title for book in books] == ["The Lord of the Rings", "The Hobbit"]


def test_repository_updates_a_book(session: Session) -> None:
    repository = BookRepository(session)
    book = repository.create(make_book("The Hobbit"))
    book.title = "The Hobbit: Revised"

    updated = repository.update(book)

    assert updated.title == "The Hobbit: Revised"
    assert repository.get_by_id(book.id).title == "The Hobbit: Revised"


def test_repository_deletes_a_book(session: Session) -> None:
    repository = BookRepository(session)
    book = repository.create(make_book("The Hobbit"))

    repository.delete(book)

    assert repository.get_by_id(book.id) is None


def test_repository_searches_by_title_or_author_case_insensitively(session: Session) -> None:
    repository = BookRepository(session)
    repository.create(make_book("O Hobbit"))
    repository.create(Book(
        title="Dom Casmurro",
        author="Machado de Assis",
        publication_date=date(1899, 1, 1),
        summary="Um clássico brasileiro.",
    ))

    title_results = repository.search(title="hobbit")
    author_results = repository.search(author="MACHADO")
    combined_results = repository.search(title="inexistente", author="assis")

    assert [book.title for book in title_results] == ["O Hobbit"]
    assert [book.title for book in author_results] == ["Dom Casmurro"]
    assert [book.title for book in combined_results] == ["Dom Casmurro"]

