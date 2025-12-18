
from typing import Dict, Any
from chalice import Response
from chalicelib.services.user_service import UserService
from chalicelib.utils.exceptions import (
    ValidationException,
    AuthenticationException,
    ConflictException,
    APIException
)
from chalicelib.utils.docs_decorator import document_endpoint
from chalicelib.docs.auth_docs import (
    REGISTER_USER_DOC,
    LOGIN_USER_DOC,
    LOGOUT_USER_DOC
)


def register_user_routes(app):
    from app import cors_config

    @app.route('/auth/register', methods=['POST'], cors=cors_config)
    @document_endpoint(**REGISTER_USER_DOC)
    def register():
        try:
            request = app.current_request
            body: Dict[str, Any] = request.json_body
            result, status_code = UserService.register(body)
            return Response(body=result, status_code=status_code)
        except ConflictException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except ValidationException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)

    @app.route('/auth/login', methods=['POST'], cors=cors_config)
    @document_endpoint(**LOGIN_USER_DOC)
    def login():
        try:
            request = app.current_request
            body: Dict[str, Any] = request.json_body
            result, status_code = UserService.login(body)
            return Response(body=result, status_code=status_code)
        except AuthenticationException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except ValidationException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)

    @app.route('/auth/logout', methods=['POST'], cors=cors_config)
    @document_endpoint(**LOGOUT_USER_DOC)
    def logout():
        try:
            request = app.current_request
            auth_header: str = request.headers.get('Authorization', '')
            token: str = auth_header[7:] if auth_header.startswith('Bearer ') else None
            result, status_code = UserService.logout(token)
            return Response(body=result, status_code=status_code)
        except AuthenticationException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
        except APIException as e:
            return Response(body={'error': e.message}, status_code=e.status_code)
