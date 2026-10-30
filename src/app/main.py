from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.controller.book_controller import router as book_router
from app.database import Base, engine
from app.model import book  # noqa: F401
from app.middleware.rate_limit import RateLimitMiddleware
from app.service.book_service import BookNotFoundError
from app.config import get_settings


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Books API",
    description="A layered CRUD API for managing books.",
    version="1.0.0",
)
settings = get_settings()
app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)


@app.exception_handler(BookNotFoundError)
def book_not_found_handler(request: Request, exc: BookNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(book_router, prefix="/api/v1")

