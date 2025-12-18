
from typing import Dict, Optional, Tuple, Any
from chalicelib.constants.api import (
    DEFAULT_PAGE, DEFAULT_PER_PAGE, MAX_PER_PAGE
)
from chalicelib.utils.exceptions import ValidationException


def parse_query_params(query_params: Dict[str, str]) -> Dict[str, Any]:
    parsed = {
        'page': DEFAULT_PAGE,
        'per_page': DEFAULT_PER_PAGE,
        'author': query_params.get('author'),
        'year': None,
        'title': query_params.get('title'),
    }

    if query_params.get('page'):
        try:
            page = int(query_params['page'])
            if page < 1:
                raise ValueError("Page must be greater than 0")
            parsed['page'] = page
        except ValueError as e:
            raise ValidationException(f"Invalid page parameter: {str(e)}")

    if query_params.get('per_page'):
        try:
            per_page = int(query_params['per_page'])
            if per_page < 1 or per_page > MAX_PER_PAGE:
                raise ValueError(f"per_page must be between 1 and {MAX_PER_PAGE}")
            parsed['per_page'] = per_page
        except ValueError as e:
            raise ValidationException(f"Invalid per_page parameter: {str(e)}")

    if query_params.get('year'):
        try:
            year = int(query_params['year'])
            if year < 1000 or year > 2100:
                raise ValueError("Year must be between 1000 and 2100")
            parsed['year'] = year
        except ValueError as e:
            raise ValidationException(f"Invalid year parameter: {str(e)}")

    return parsed
