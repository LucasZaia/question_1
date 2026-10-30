from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)


class BookFields(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    publication_date: date
    summary: str = Field(min_length=1)


class BookCreate(BookFields):
    pass


class BookUpdate(BookFields):
    pass


class BookResponse(BookFields):
    id: int

    model_config = ConfigDict(from_attributes=True)

