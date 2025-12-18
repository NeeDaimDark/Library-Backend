
from pydantic import BaseModel, field_validator, Field
from typing import Optional
from chalicelib.validators import book_validators


class Book(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=255, description="Book title")
    author: str = Field(..., min_length=1, max_length=255, description="Author name")
    year: Optional[int] = Field(None, ge=1000, description="Publication year")
    isbn: Optional[str] = Field(None, min_length=10, max_length=20, description="ISBN-10 or ISBN-13")
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        return book_validators.BookValidator.validate_not_empty(v)

    @field_validator('year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        return book_validators.BookValidator.validate_year(v)

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        return book_validators.BookValidator.validate_isbn(v)


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Book title (required)")
    author: str = Field(..., min_length=1, max_length=255, description="Author name (required)")
    year: Optional[int] = Field(None, ge=1000, description="Publication year (optional)")
    isbn: Optional[str] = Field(None, min_length=10, max_length=17, description="ISBN number (optional)")

    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        return book_validators.BookValidator.validate_not_empty(v)

    @field_validator('year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        return book_validators.BookValidator.validate_year_not_future(v)

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        return book_validators.BookValidator.validate_isbn_optional(v)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Book title (optional)")
    author: Optional[str] = Field(None, min_length=1, max_length=255, description="Author name (optional)")
    year: Optional[int] = Field(None, ge=1000, description="Publication year (optional)")
    isbn: Optional[str] = Field(None, min_length=10, max_length=17, description="ISBN number (optional)")

    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty(cls, v: Optional[str]) -> Optional[str]:
        return book_validators.BookValidator.validate_not_empty_optional(v)

    @field_validator('year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        return book_validators.BookValidator.validate_year_not_future(v)

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        return book_validators.BookValidator.validate_isbn_optional(v)