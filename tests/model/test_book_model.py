from datetime import date

import pytest
from pydantic import ValidationError

from app.model.book import BookCreate, BookResponse, BookUpdate


def test_book_create_accepts_valid_data() -> None:
    book = BookCreate(
        title="The Hobbit",
        author="J. R. R. Tolkien",
        publication_date="1937-09-21",
        summary="A hobbit goes on an unexpected journey.",
    )

    assert book.publication_date == date(1937, 9, 21)


def test_book_create_rejects_missing_or_invalid_values() -> None:
    with pytest.raises(ValidationError):
        BookCreate(
            title="",
            author="J. R. R. Tolkien",
            publication_date="not-a-date",
            summary="Summary",
        )


def test_book_response_serializes_an_orm_object() -> None:
    class BookRecord:
        id = 1
        title = "The Hobbit"
        author = "J. R. R. Tolkien"
        publication_date = date(1937, 9, 21)
        summary = "A hobbit goes on an unexpected journey."

    response = BookResponse.model_validate(BookRecord(), from_attributes=True)

    assert response.id == 1
    assert response.model_dump()["publication_date"] == date(1937, 9, 21)


def test_book_update_has_the_same_fields_as_put_contract() -> None:
    update = BookUpdate(
        title="The Hobbit: Revised",
        author="J. R. R. Tolkien",
        publication_date=date(1937, 9, 21),
        summary="An updated summary.",
    )

    assert update.title == "The Hobbit: Revised"

