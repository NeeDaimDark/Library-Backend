
from typing import Dict, Any, Optional, Tuple
from chalice import Response
from chalicelib.services.user_service import UserService
from chalicelib.utils.exceptions import AuthenticationException
from chalicelib.constants.api import ERROR_UNAUTHORIZED


def get_auth_token(request) -> Optional[str]:
    auth_header: str = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return None


def require_auth(request) -> Tuple[Optional[Dict[str, Any]], Optional[Response]]:
    token: Optional[str] = get_auth_token(request)
    user: Optional[Dict[str, Any]] = UserService.verify_token(token)

    if not user:
        return None, Response(
            body={'error': 'Unauthorized', 'message': ERROR_UNAUTHORIZED},
            status_code=401
        )

    return user, None
