
from typing import Dict, Any
from chalice import Response
from chalicelib.services.book_service import BookService
from chalicelib.middleware.auth_middleware import require_auth
from chalicelib.utils.validators import parse_query_params
from chalicelib.utils.exceptions import (
    ValidationException,
    NotFoundException,
    APIException
)
from chalicelib.utils.docs_decorator import document_endpoint
from chalicelib.docs.book_docs import (
    CREATE_BOOK_DOC,
    GET_ALL_BOOKS_DOC,
    GET_BOOK_DOC,
    UPDATE_BOOK_DOC,
    DELETE_BOOK_DOC
)


def register_book_routes(app):
    from app import cors_config

    @app.route('/books', methods=['POST'], cors=cors_config)
    @document_endpoint(**CREATE_BOOK_DOC)
    def create_book():
        try:
            request = app.current_request

            _, error_response = require_auth(request)
            if error_response:
                return error_response

            body: Dict[str, Any] = request.json_body
            result, status_code = BookService.create_book(body)
            return Response(body=result, status_code=status_code)
        except ValidationException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)

    @app.route('/books', methods=['GET'], cors=cors_config)
    @document_endpoint(**GET_ALL_BOOKS_DOC)
    def get_all_books():
        try:
            request = app.current_request
            query_params: Dict[str, Any] = request.query_params or {}

            parsed_params: Dict[str, Any] = parse_query_params(query_params)
            result, status_code = BookService.get_all_books(**parsed_params)
            return Response(body=result, status_code=status_code)
        except ValidationException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)

    @app.route('/books/{book_id}', methods=['GET'], cors=cors_config)
    @document_endpoint(**GET_BOOK_DOC)
    def get_book(book_id):
        try:
            result, status_code = BookService.get_book(int(book_id))
            return Response(body=result, status_code=status_code)
        except NotFoundException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)

    @app.route('/books/{book_id}', methods=['PUT'], cors=cors_config)
    @document_endpoint(**UPDATE_BOOK_DOC)
    def update_book(book_id):
        try:
            request = app.current_request

            _, error_response = require_auth(request)
            if error_response:
                return error_response

            body: Dict[str, Any] = request.json_body
            result, status_code = BookService.update_book(int(book_id), body)
            return Response(body=result, status_code=status_code)
        except ValidationException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except NotFoundException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)

    @app.route('/books/{book_id}', methods=['DELETE'], cors=cors_config)
    @document_endpoint(**DELETE_BOOK_DOC)
    def delete_book(book_id):
        try:
            request = app.current_request

            _, error_response = require_auth(request)
            if error_response:
                return error_response

            result, status_code = BookService.delete_book(int(book_id))
            return Response(body=result, status_code=status_code)
        except NotFoundException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
