from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.book import BookCreate, BookResponse, BookUpdate
from app.service.book_service import BookService


router = APIRouter(prefix="/books", tags=["books"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_book_service(db: DatabaseSession) -> BookService:
    return BookService(db)


BookServiceDependency = Annotated[BookService, Depends(get_book_service)]


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, service: BookServiceDependency) -> BookResponse:
    return service.create(book_data)


@router.get("", response_model=list[BookResponse])
def list_books(service: BookServiceDependency) -> list[BookResponse]:
    return service.list_all()


@router.get("/search", response_model=list[BookResponse])
def search_books(
    service: BookServiceDependency,
    title: str | None = Query(default=None, min_length=1),
    author: str | None = Query(default=None, min_length=1),
) -> list[BookResponse]:
    if title is None and author is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one search parameter is required: title or author",
        )
    return service.search(title=title, author=author)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, service: BookServiceDependency) -> BookResponse:
    return service.get_by_id(book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    service: BookServiceDependency,
) -> BookResponse:
    return service.update(book_id, book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, service: BookServiceDependency) -> None:
    service.delete(book_id)

