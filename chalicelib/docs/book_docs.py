CREATE_BOOK_DOC = {
    'summary': 'Create a new book',
    'description': 'Create a new book entry in the library (requires authentication)',
    'tags': ['Books'],
    'request_body': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'required': ['title', 'author'],
                    'properties': {
                        'title': {'type': 'string', 'example': 'The Great Gatsby'},
                        'author': {'type': 'string', 'example': 'F. Scott Fitzgerald'},
                        'year': {'type': 'integer', 'example': 1925},
                        'isbn': {'type': 'string', 'example': '978-0-7432-7356-5'}
                    }
                }
            }
        }
    },
    'responses': {
        201: 'Book created successfully',
        400: 'Validation error',
        401: 'Unauthorized - JWT token required'
    },
    'security': ['BearerAuth']
}

GET_ALL_BOOKS_DOC = {
    'summary': 'Get all books',
    'description': 'Retrieve all books with optional pagination and filtering',
    'tags': ['Books'],
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'schema': {'type': 'integer', 'default': 1},
            'description': 'Page number for pagination'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'schema': {'type': 'integer', 'default': 10},
            'description': 'Number of books per page'
        },
        {
            'name': 'title',
            'in': 'query',
            'schema': {'type': 'string'},
            'description': 'Filter by book title'
        },
        {
            'name': 'author',
            'in': 'query',
            'schema': {'type': 'string'},
            'description': 'Filter by author name'
        },
        {
            'name': 'year',
            'in': 'query',
            'schema': {'type': 'integer'},
            'description': 'Filter by publication year'
        }
    ],
    'responses': {
        200: 'List of books retrieved successfully',
        400: 'Invalid query parameters'
    }
}

GET_BOOK_DOC = {
    'summary': 'Get book by ID',
    'description': 'Retrieve a specific book by its ID',
    'tags': ['Books'],
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'required': True,
            'schema': {'type': 'integer'},
            'description': 'The ID of the book'
        }
    ],
    'responses': {
        200: 'Book found',
        404: 'Book not found'
    }
}

UPDATE_BOOK_DOC = {
    'summary': 'Update a book',
    'description': 'Update an existing book (requires authentication)',
    'tags': ['Books'],
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'required': True,
            'schema': {'type': 'integer'},
            'description': 'The ID of the book to update'
        }
    ],
    'request_body': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'author': {'type': 'string'},
                        'year': {'type': 'integer'},
                        'isbn': {'type': 'string'}
                    }
                }
            }
        }
    },
    'responses': {
        200: 'Book updated successfully',
        404: 'Book not found',
        401: 'Unauthorized - JWT token required'
    },
    'security': ['BearerAuth']
}

DELETE_BOOK_DOC = {
    'summary': 'Delete a book',
    'description': 'Delete a book from the library (requires authentication)',
    'tags': ['Books'],
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'required': True,
            'schema': {'type': 'integer'},
            'description': 'The ID of the book to delete'
        }
    ],
    'responses': {
        200: 'Book deleted successfully',
        404: 'Book not found',
        401: 'Unauthorized - JWT token required'
    },
    'security': ['BearerAuth']
}
