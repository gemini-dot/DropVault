class AppException(Exception):
    """
    Base exception for the application.

    This exception is used as the parent class for all custom exceptions
    in the system. It standardizes error handling by carrying structured
    information that can be used by global exception handlers to build
    consistent API responses.

    Attributes:
        message (str): Human-readable error message.
        code (str): Machine-readable error code (for frontend / logging).
        status_code (int): HTTP status code to return (default: 500).
        data (dict): Optional extra metadata about the error.
    """

    def __init__(self, message: str, code: str, status_code: int = 500, data=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.data = data or {}


class AuthenticationError(AppException):
    """
    Exception raised for authentication failures.
    """

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, code="AUTH_FAILED", status_code=401)


class AuthorizationError(AppException):
    """
    Exception raised for authorization failures (e.g., insufficient permissions).
    """

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message=message, code="UNAUTHORIZED", status_code=403)
