import re
from typing import Optional
from chalicelib.constants.validation_errors import (
    USERNAME_EMPTY,
    USERNAME_INVALID_CHARS,
    PASSWORD_EMPTY,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MISSING_LETTER,
    PASSWORD_MISSING_NUMBER,
    FIELD_EMPTY
)


class UserValidator:

    @staticmethod
    def validate_username(v: str) -> str:
        if not v or not v.strip():
            raise ValueError(USERNAME_EMPTY)
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError(USERNAME_INVALID_CHARS)
        return v.strip()

    @staticmethod
    def validate_password(v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v or not v.strip():
            raise ValueError(PASSWORD_EMPTY)
        if len(v) < 6:
            raise ValueError(PASSWORD_MIN_LENGTH)
        if not re.search(r'[A-Za-z]', v):
            raise ValueError(PASSWORD_MISSING_LETTER)
        if not re.search(r'\d', v):
            raise ValueError(PASSWORD_MISSING_NUMBER)
        return v

    @staticmethod
    def validate_password_required(v: str) -> str:
        if not v or not v.strip():
            raise ValueError(PASSWORD_EMPTY)
        if len(v) < 6:
            raise ValueError(PASSWORD_MIN_LENGTH)
        if not re.search(r'[A-Za-z]', v):
            raise ValueError(PASSWORD_MISSING_LETTER)
        if not re.search(r'\d', v):
            raise ValueError(PASSWORD_MISSING_NUMBER)
        return v

    @staticmethod
    def validate_not_empty(v: str) -> str:
        if not v or not v.strip():
            raise ValueError(FIELD_EMPTY)
        return v.strip()
