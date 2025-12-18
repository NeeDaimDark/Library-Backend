REGISTER_USER_DOC = {
    'summary': 'Register a new user',
    'description': 'Create a new user account with username, email, and password',
    'tags': ['Authentication'],
    'request_body': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'required': ['username', 'email', 'password'],
                    'properties': {
                        'username': {'type': 'string', 'example': 'john_doe'},
                        'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
                        'password': {'type': 'string', 'format': 'password', 'example': 'securepass123'}
                    }
                }
            }
        }
    },
    'responses': {
        201: 'User registered successfully',
        400: 'Validation error',
        409: 'User already exists'
    }
}

LOGIN_USER_DOC = {
    'summary': 'Login user and get JWT token',
    'description': 'Authenticate user and return JWT token for protected endpoints',
    'tags': ['Authentication'],
    'request_body': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'required': ['username', 'password'],
                    'properties': {
                        'username': {'type': 'string', 'example': 'john_doe'},
                        'password': {'type': 'string', 'format': 'password', 'example': 'securepass123'}
                    }
                }
            }
        }
    },
    'responses': {
        200: 'Login successful, returns JWT token',
        401: 'Invalid credentials',
        404: 'User not found'
    }
}

LOGOUT_USER_DOC = {
    'summary': 'Logout user',
    'description': 'Logout user by invalidating their JWT token',
    'tags': ['Authentication'],
    'security': [{'Bearer': []}],
    'responses': {
        200: 'Logout successful',
        401: 'Unauthorized - Invalid or missing token'
    }
}
