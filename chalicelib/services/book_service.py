
from typing import Dict, Optional, Any, Tuple, List
from chalicelib.repositories.book_repository import BookRepository
from chalicelib.pagination.book_pagination import BookPagination
from chalicelib.models import book_model
from chalicelib.utils.exceptions import ValidationException, NotFoundException
from chalicelib.constants.api import (
    SUCCESS_BOOK_CREATED,
    SUCCESS_BOOK_UPDATED,
    SUCCESS_BOOK_DELETED,
    ERROR_BOOK_NOT_FOUND
)
from pydantic import ValidationError


class BookService:

    @staticmethod
    def _format_validation_errors(validation_error: ValidationError) -> List[Dict[str, Any]]:
        errors: List[Dict[str, Any]] = []
        for error in validation_error.errors():
            errors.append({
                'field': '.'.join(str(loc) for loc in error['loc']),
                'message': error['msg'],
                'type': error['type']
            })
        return errors

    @staticmethod
    def create_book(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        try:
            book_data: book_model.BookCreate = book_model.BookCreate(**data)

            book_id: int = BookRepository.create(
                title=book_data.title,
                author=book_data.author,
                year=book_data.year,
                isbn=book_data.isbn
            )
            return {
                'message': SUCCESS_BOOK_CREATED,
                'book_id': book_id
            }, 201

        except ValidationError as e:
            raise ValidationException(f"Book validation failed: {str(e)}")
        except Exception as e:
            raise ValidationException(f"Error creating book: {str(e)}")

    @staticmethod
    def get_all_books(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
        title: Optional[str] = None
    ) -> Tuple[Dict[str, Any], int]:
        try:
            if page is not None and per_page is not None:
                if page < 1:
                    raise ValidationException("Page number must be >= 1")
                if per_page < 1 or per_page > 100:
                    raise ValidationException("Per page must be between 1 and 100")

                if year is not None:
                    if year < 1000 or year > 2100:
                        raise ValidationException("Year must be between 1000 and 2100")

                result: Dict[str, Any] = BookPagination.paginate(
                    page=page,
                    per_page=per_page,
                    author=author,
                    year=year,
                    title=title
                )
                return result, 200
            else:
                books: List[Dict[str, Any]] = BookRepository.find_all()
                return {'books': books}, 200

        except ValidationException:
            raise
        except Exception as e:
            raise ValidationException(f"Error fetching books: {str(e)}")

    @staticmethod
    def get_book(book_id: int) -> Tuple[Dict[str, Any], int]:
        try:
            book: Optional[Dict[str, Any]] = BookRepository.find_by_id(book_id)
            if book:
                return {'book': book}, 200
            else:
                raise NotFoundException(ERROR_BOOK_NOT_FOUND)
        except NotFoundException:
            raise
        except Exception as e:
            raise NotFoundException(ERROR_BOOK_NOT_FOUND)

    @staticmethod
    def update_book(book_id: int, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        try:
            book_data: book_model.BookUpdate = book_model.BookUpdate(**data)

            success: bool = BookRepository.update(
                book_id=book_id,
                title=book_data.title,
                author=book_data.author,
                year=book_data.year,
                isbn=book_data.isbn
            )

            if success:
                return {'message': SUCCESS_BOOK_UPDATED}, 200
            else:
                raise NotFoundException(ERROR_BOOK_NOT_FOUND)

        except NotFoundException:
            raise
        except ValidationError as e:
            raise ValidationException(f"Book validation failed: {str(e)}")
        except Exception as e:
            raise ValidationException(f"Error updating book: {str(e)}")

    @staticmethod
    def delete_book(book_id: int) -> Tuple[Dict[str, Any], int]:
        try:
            success: bool = BookRepository.delete(book_id)
            if success:
                return {'message': SUCCESS_BOOK_DELETED}, 200
            else:
                raise NotFoundException(ERROR_BOOK_NOT_FOUND)
        except NotFoundException:
            raise
        except Exception as e:
            raise NotFoundException(ERROR_BOOK_NOT_FOUND)
