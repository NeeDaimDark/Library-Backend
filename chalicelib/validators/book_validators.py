from typing import Optional
from datetime import datetime
from chalicelib.constants.validation_errors import (
    FIELD_EMPTY,
    YEAR_RANGE,
    YEAR_FUTURE,
    ISBN_LENGTH,
    ISBN_10_INVALID,
    ISBN_13_INVALID
)


class BookValidator:

    @staticmethod
    def validate_not_empty(v: str) -> str:
        if not v or not v.strip():
            raise ValueError(FIELD_EMPTY)
        return v.strip()

    @staticmethod
    def validate_not_empty_optional(v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError(FIELD_EMPTY)
            return v.strip()
        return v

    @staticmethod
    def validate_year(v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        current_year = datetime.now().year
        if v < 1000 or v > current_year:
            raise ValueError(YEAR_RANGE.format(current_year=current_year))
        return v

    @staticmethod
    def validate_year_not_future(v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError(YEAR_FUTURE.format(current_year=current_year))
        return v

    @staticmethod
    def validate_isbn(v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not v.strip():
            return None

        isbn_clean: str = v.replace('-', '').replace(' ', '')

        if len(isbn_clean) not in [10, 13]:
            raise ValueError(ISBN_LENGTH)

        if len(isbn_clean) == 10:
            if not (isbn_clean[:-1].isdigit() and (isbn_clean[-1].isdigit() or isbn_clean[-1].upper() == 'X')):
                raise ValueError(ISBN_10_INVALID)
        else:
            if not isbn_clean.isdigit():
                raise ValueError(ISBN_13_INVALID)

        return v

    @staticmethod
    def validate_isbn_optional(v: Optional[str]) -> Optional[str]:
        if v is None:
            return v

        isbn_clean: str = v.replace('-', '').replace(' ', '')

        if len(isbn_clean) not in [10, 13]:
            raise ValueError(ISBN_LENGTH)

        if len(isbn_clean) == 10:
            if not (isbn_clean[:-1].isdigit() and (isbn_clean[-1].isdigit() or isbn_clean[-1].upper() == 'X')):
                raise ValueError(ISBN_10_INVALID)
        else:
            if not isbn_clean.isdigit():
                raise ValueError(ISBN_13_INVALID)

        return v
