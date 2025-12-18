class APIException(Exception):

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message: str = message
        self.status_code: int = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(message='{self.message}', status_code={self.status_code})"

    def __repr__(self) -> str:
        return self.__str__()


class ValidationException(APIException):

    def __init__(self, message: str) -> None:
        super().__init__(message, 400)


class AuthenticationException(APIException):

    def __init__(self, message: str) -> None:
        super().__init__(message, 401)


class AuthorizationException(APIException):

    def __init__(self, message: str) -> None:
        super().__init__(message, 403)


class NotFoundException(APIException):

    def __init__(self, message: str) -> None:
        super().__init__(message, 404)


class ConflictException(APIException):

    def __init__(self, message: str) -> None:
        super().__init__(message, 409)
