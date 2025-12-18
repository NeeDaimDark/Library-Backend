"""
Swagger/OpenAPI configuration for the Library API

This module defines the complete OpenAPI 3.0 specification for the Library API,
including all endpoints, schemas, security schemes, and documentation.
"""


OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Library API - Book Management System",
        "version": "1.0.0",
        "description": "A RESTful API for managing a library book collection",
        "contact": {
            "name": "Library API Support",
            "email": "support@library-api.com"
        }
    },
    "servers": [
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        }
    ],
    "tags": [
        {
            "name": "Authentication",
            "description": "User registration and login endpoints"
        },
        {
            "name": "Books",
            "description": "Book management operations (CRUD)"
        }
    ],
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT Authorization header using the Bearer scheme"
            }
        },
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                }
            },
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "year": {"type": "integer"},
                    "isbn": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"}
                }
            },
            "UserRegister": {
                "type": "object",
                "required": ["username", "email", "password"],
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string", "format": "password"}
                }
            },
            "UserLogin": {
                "type": "object",
                "required": ["username", "password"],
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string", "format": "password"}
                }
            },
            "BookCreate": {
                "type": "object",
                "required": ["title", "author"],
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "year": {"type": "integer"},
                    "isbn": {"type": "string"}
                }
            },
            "BookUpdate": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "year": {"type": "integer"},
                    "isbn": {"type": "string"}
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "message": {"type": "string"}
                }
            }
        }
    },
    "paths": {
        "/auth/register": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Register a new user",
                "description": "Create a new user account",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserRegister"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "User registered successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string"},
                                        "user_id": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Validation error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        },
        "/auth/login": {
            "post": {
                "tags": ["Authentication"],
                "summary": "Login user",
                "description": "Login and get JWT token",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserLogin"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "token": {"type": "string"},
                                        "user_id": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Invalid credentials",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        },
        "/books": {
            "post": {
                "tags": ["Books"],
                "summary": "Create a new book",
                "description": "Create a new book entry (requires authentication)",
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/BookCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Book created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string"},
                                        "book_id": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Validation error"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            },
            "get": {
                "tags": ["Books"],
                "summary": "Get all books",
                "description": "Retrieve all books with optional pagination and filtering",
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Page number for pagination",
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Number of books per page",
                        "schema": {"type": "integer", "default": 10}
                    },
                    {
                        "name": "title",
                        "in": "query",
                        "description": "Filter by book title",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "author",
                        "in": "query",
                        "description": "Filter by book author",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "year",
                        "in": "query",
                        "description": "Filter by publication year",
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "List of books",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "books": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Book"}
                                        },
                                        "total": {"type": "integer"},
                                        "page": {"type": "integer"},
                                        "per_page": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/books/{book_id}": {
            "get": {
                "tags": ["Books"],
                "summary": "Get book by ID",
                "description": "Retrieve a specific book by ID",
                "parameters": [
                    {
                        "name": "book_id",
                        "in": "path",
                        "required": True,
                        "description": "Book ID",
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Book found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Book"}
                            }
                        }
                    },
                    "404": {
                        "description": "Book not found"
                    }
                }
            },
            "put": {
                "tags": ["Books"],
                "summary": "Update book",
                "description": "Update a book by ID (requires authentication)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "book_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/BookUpdate"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Book updated successfully"
                    },
                    "404": {
                        "description": "Book not found"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            },
            "delete": {
                "tags": ["Books"],
                "summary": "Delete book",
                "description": "Delete a book by ID (requires authentication)",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "book_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Book deleted successfully"
                    },
                    "404": {
                        "description": "Book not found"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        }
    }
}


def init_swagger(app):
    """
    Initialize Swagger documentation for the Chalice app.
    
    Args:
        app: Chalice application instance
        
    Returns:
        dict: OpenAPI specification dictionary
    """
    return OPENAPI_SPEC
