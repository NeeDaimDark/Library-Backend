JWT_SECRET_KEY = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRATION_HOURS = 24

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 100

MIN_PASSWORD_LENGTH = 8
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50
MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 255
MIN_AUTHOR_LENGTH = 1
MAX_AUTHOR_LENGTH = 255

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409

ERROR_INVALID_EMAIL = "Invalid email format"
ERROR_INVALID_PASSWORD = "Password must be at least {} characters long"
ERROR_USERNAME_EXISTS = "Username already exists"
ERROR_USER_NOT_FOUND = "User not found"
ERROR_INVALID_CREDENTIALS = "Invalid username or password"
ERROR_UNAUTHORIZED = "Unauthorized - Invalid or missing authentication token"
ERROR_BOOK_NOT_FOUND = "Book not found"
ERROR_VALIDATION_ERROR = "Validation error"
ERROR_MISSING_REQUIRED_FIELD = "Missing required field: {}"

SUCCESS_USER_REGISTERED = "User registered successfully"
SUCCESS_LOGIN = "Login successful"
SUCCESS_BOOK_CREATED = "Book created successfully"
SUCCESS_BOOK_UPDATED = "Book updated successfully"
SUCCESS_BOOK_DELETED = "Book deleted successfully"
