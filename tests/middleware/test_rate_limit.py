from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.rate_limit import RateLimitMiddleware


def create_test_app() -> FastAPI:
    test_app = FastAPI()
    test_app.add_middleware(RateLimitMiddleware, max_requests=2, window_seconds=60)

    @test_app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return test_app


def test_rate_limit_is_applied_per_ip() -> None:
    client = TestClient(create_test_app())

    first_response = client.get("/health")
    second_response = client.get("/health")
    limited_response = client.get("/health")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert limited_response.status_code == 429
    assert limited_response.json()["detail"] == "Rate limit exceeded"
    assert limited_response.headers["Retry-After"] == "60"


def test_rate_limit_headers_are_returned_for_allowed_requests() -> None:
    client = TestClient(create_test_app())

    response = client.get("/health")

    assert response.headers["X-RateLimit-Limit"] == "2"
    assert response.headers["X-RateLimit-Remaining"] == "1"

