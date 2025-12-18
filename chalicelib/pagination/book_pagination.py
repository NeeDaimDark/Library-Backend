from typing import Optional, Dict, List, Any
from chalicelib.database.db import db_connection
from chalicelib.constants import db_queries


class BookPagination:

    @staticmethod
    def paginate(
        page: int = 1,
        per_page: int = 10,
        author: Optional[str] = None,
        year: Optional[int] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        with db_connection() as conn:
            cursor = conn.cursor()

            query: str = db_queries.BookQueries.SELECT_BOOKS_BASE
            count_query: str = db_queries.BookQueries.COUNT_BOOKS_BASE
            params: List[Any] = []
            count_params: List[Any] = []

            if author:
                query += db_queries.BookQueries.FILTER_BY_AUTHOR
                count_query += db_queries.BookQueries.FILTER_BY_AUTHOR
                filter_value: str = f'%{author}%'
                params.append(filter_value)
                count_params.append(filter_value)

            if year:
                query += db_queries.BookQueries.FILTER_BY_YEAR
                count_query += db_queries.BookQueries.FILTER_BY_YEAR
                params.append(year)
                count_params.append(year)

            if title:
                query += db_queries.BookQueries.FILTER_BY_TITLE
                count_query += db_queries.BookQueries.FILTER_BY_TITLE
                filter_value: str = f'%{title}%'
                params.append(filter_value)
                count_params.append(filter_value)

            offset: int = (page - 1) * per_page

            total_count: int = cursor.execute(count_query, count_params).fetchone()['count']

            query += db_queries.BookQueries.PAGINATION_SUFFIX
            params.extend([per_page, offset])

            books: List[Any] = cursor.execute(query, params).fetchall()

            return {
                'books': [dict(book) for book in books],
                'total': total_count,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_count + per_page - 1) // per_page if total_count > 0 else 0,
                'filters': {
                    'author': author,
                    'year': year,
                    'title': title
                }
            }
