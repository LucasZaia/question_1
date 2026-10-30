from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_get_db() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def payload() -> dict[str, str]:
    return {
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "publication_date": "1937-09-21",
        "summary": "A hobbit goes on an unexpected journey.",
    }


def test_book_crud_endpoints(client: TestClient) -> None:
    create_response = client.post("/api/v1/books", json=payload())
    assert create_response.status_code == 201
    book = create_response.json()
    assert book["title"] == "The Hobbit"

    book_id = book["id"]
    assert client.get("/api/v1/books").json()[0]["id"] == book_id
    assert client.get(f"/api/v1/books/{book_id}").status_code == 200

    update_payload = {**payload(), "title": "The Hobbit: Revised"}
    update_response = client.put(f"/api/v1/books/{book_id}", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "The Hobbit: Revised"

    delete_response = client.delete(f"/api/v1/books/{book_id}")
    assert delete_response.status_code == 204
    assert client.get(f"/api/v1/books/{book_id}").status_code == 404


def test_controller_returns_validation_and_not_found_errors(client: TestClient) -> None:
    invalid_response = client.post("/api/v1/books", json={**payload(), "publication_date": "invalid"})
    assert invalid_response.status_code == 422
    assert client.get("/api/v1/books/999").status_code == 404
    assert client.put("/api/v1/books/999", json=payload()).status_code == 404
    assert client.delete("/api/v1/books/999").status_code == 404


def test_controller_searches_by_title_or_author(client: TestClient) -> None:
    client.post("/api/v1/books", json=payload())

    response = client.get("/api/v1/books/search?title=HOBBIT")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "The Hobbit"

