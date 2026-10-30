from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.model.book import BookCreate, BookUpdate
from app.service.book_service import BookNotFoundError, BookService


@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as database_session:
        yield database_session


def book_data(title: str = "The Hobbit") -> BookCreate:
    return BookCreate(
        title=title,
        author="J. R. R. Tolkien",
        publication_date=date(1937, 9, 21),
        summary="A hobbit goes on an unexpected journey.",
    )


def updated_book_data() -> BookUpdate:
    return BookUpdate(
        title="The Hobbit: Revised",
        author="J. R. R. Tolkien",
        publication_date=date(1937, 9, 21),
        summary="An updated summary.",
    )


def test_service_lists_no_books_for_a_new_database(session: Session) -> None:
    service = BookService(session)

    assert service.list_all() == []


def test_service_creates_and_retrieves_a_book(session: Session) -> None:
    service = BookService(session)

    created = service.create(book_data())

    assert created.id is not None
    assert service.get_by_id(created.id).author == "J. R. R. Tolkien"

    assert service.list_all()[0].title == "The Hobbit"


def test_service_updates_a_book(session: Session) -> None:
    service = BookService(session)
    created = service.create(book_data())

    updated = service.update(created.id, updated_book_data())

    assert updated.title == "The Hobbit: Revised"


def test_service_deletes_a_book(session: Session) -> None:
    service = BookService(session)
    created = service.create(book_data())

    service.delete(created.id)

    assert service.list_all() == []


@pytest.mark.parametrize("operation", ["get_by_id", "delete"])
def test_service_raises_for_missing_book(session: Session, operation: str) -> None:
    service = BookService(session)

    with pytest.raises(BookNotFoundError):
        getattr(service, operation)(999)


def test_service_raises_when_updating_a_missing_book(session: Session) -> None:
    service = BookService(session)

    with pytest.raises(BookNotFoundError):
        service.update(999, updated_book_data())


def test_service_searches_books_by_title_or_author(session: Session) -> None:
    service = BookService(session)
    service.create(book_data("O Hobbit"))

    results = service.search(title="hobbit")

    assert [book.title for book in results] == ["O Hobbit"]

