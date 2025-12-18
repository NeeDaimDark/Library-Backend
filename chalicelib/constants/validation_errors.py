"""
Validation error message constants for validators.
"""

# User Validator Error Messages
USERNAME_EMPTY = 'Username cannot be empty or whitespace'
USERNAME_INVALID_CHARS = 'Username can only contain letters, numbers, and underscores'
PASSWORD_EMPTY = 'Password cannot be empty or whitespace'
PASSWORD_MIN_LENGTH = 'Password must be at least 6 characters long'
PASSWORD_MISSING_LETTER = 'Password must contain at least one letter'
PASSWORD_MISSING_NUMBER = 'Password must contain at least one number'
FIELD_EMPTY = 'Field cannot be empty or whitespace'

# Book Validator Error Messages
YEAR_RANGE = 'Year must be between 1000 and {current_year}'
YEAR_FUTURE = 'Year cannot be greater than {current_year}'
ISBN_LENGTH = 'ISBN must be 10 or 13 characters (excluding hyphens)'
ISBN_10_INVALID = 'Invalid ISBN-10 format'
ISBN_13_INVALID = 'Invalid ISBN-13 format'
