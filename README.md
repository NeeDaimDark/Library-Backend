# Library API - Book Management System

A RESTful API backend for managing a library book collection with user authentication and authorization.

## Technology Stack

- **Framework**: AWS Chalice (Python serverless framework)
- **Database**: SQLite3
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **ORM**: Raw SQL queries with SQLite3

## Features

- User registration and authentication with JWT tokens
- Full CRUD operations for books
- Pagination and filtering for book listings
- Field validation for all inputs
- ISBN-10 and ISBN-13 validation
- Protected endpoints requiring authentication

## Project Structure

```
library-api-project/
├── app.py                          # Main application entry point
├── chalicelib/
│   ├── constants/                  # Application constants
│   │   ├── api.py                  # API constants (JWT, HTTP codes, messages)
│   │   ├── db_queries.py           # SQL query constants
│   │   └── validation_errors.py    # Validation error messages
│   ├── controllers/                # Route handlers
│   │   ├── book_controller.py      # Book CRUD endpoints
│   │   ├── user_controller.py      # Auth endpoints
│   │   └── doc_controller.py       # Documentation endpoints
│   ├── database/
│   │   └── db.py                   # Database connection & initialization
│   ├── middleware/
│   │   └── auth_middleware.py      # JWT authentication middleware
│   ├── models/                     # Pydantic models
│   │   ├── book_model.py           # Book, BookCreate, BookUpdate
│   │   └── user_model.py           # User, UserRegister, UserLogin
│   ├── pagination/
│   │   └── book_pagination.py      # Pagination logic for books
│   ├── repositories/               # Data access layer
│   │   ├── book_repository.py      # Book database operations
│   │   └── user_repository.py      # User database operations
│   ├── services/                   # Business logic layer
│   │   ├── book_service.py         # Book business logic
│   │   └── user_service.py         # Auth & user business logic
│   ├── utils/                      # Utility modules
│   │   ├── exceptions.py           # Custom exception classes
│   │   └── validators.py           # Query parameter validators
│   └── validators/                 # Field validators
│       ├── book_validators.py      # Book field validation
│       └── user_validators.py      # User field validation
├── requirements.txt                # Python dependencies
└── test_complete_api.py           # Comprehensive API test suite
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip
- virtualenv

### Setup Steps

1. **Clone the repository**
   ```bash
   cd library-api-project
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   chalice local --port 8000
   ```

5. **The API will be available at**: `http://127.0.0.1:8000`

## API Endpoints

### Base URL
```
http://127.0.0.1:8000
```

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (201)**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response (200)**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Book Endpoints

#### Get All Books
```http
GET /books
```

**Query Parameters (optional):**
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10, max: 100)
- `author` - Filter by author (partial match)
- `year` - Filter by publication year
- `title` - Filter by title (partial match)

**Example:**
```http
GET /books?page=1&per_page=10&author=Martin&year=2008
```

**Response (200)**
```json
{
  "books": [
    {
      "id": 1,
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "year": 2008,
      "isbn": "978-0132350884",
      "created_at": "2024-01-15 10:30:00"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "total_pages": 1,
  "filters": {
    "author": "Martin",
    "year": 2008,
    "title": null
  }
}
```

#### Get Book by ID
```http
GET /books/{book_id}
```

**Response (200)**
```json
{
  "book": {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "year": 2008,
    "isbn": "978-0132350884",
    "created_at": "2024-01-15 10:30:00"
  }
}
```

#### Create Book (Protected)
```http
POST /books
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "year": 2008,
  "isbn": "978-0132350884"
}
```

**Response (201)**
```json
{
  "message": "Book created successfully",
  "book_id": 1
}
```

#### Update Book (Protected)
```http
PUT /books/{book_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Clean Code - Updated",
  "author": "Robert C. Martin",
  "year": 2008,
  "isbn": "978-0132350884"
}
```

**Response (200)**
```json
{
  "message": "Book updated successfully"
}
```

#### Delete Book (Protected)
```http
DELETE /books/{book_id}
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "message": "Book deleted successfully"
}
```

## Authentication

### Using JWT Tokens

After successful registration or login, you'll receive a JWT token. Include this token in the `Authorization` header for protected endpoints:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Token Expiration

- Tokens expire after **24 hours**
- You'll need to login again to get a new token

## Validation Rules

### User Validation

**Username:**
- Required
- Must contain only letters, numbers, and underscores
- 3-50 characters

**Email:**
- Required
- Must be valid email format

**Password:**
- Required
- Minimum 6 characters
- Must contain at least one letter
- Must contain at least one number

### Book Validation

**Title:**
- Required
- 1-255 characters
- Cannot be empty or whitespace

**Author:**
- Required
- 1-255 characters
- Cannot be empty or whitespace

**Year:**
- Optional
- Must be between 1000 and current year
- Cannot be in the future

**ISBN:**
- Optional
- Must be valid ISBN-10 (10 digits, last can be 'X') or ISBN-13 (13 digits)
- Hyphens and spaces are allowed and ignored

## Error Responses

### 400 Bad Request
```json
{
  "error": "Book validation failed: Year cannot be greater than 2024"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Unauthorized - Invalid or missing authentication token"
}
```

### 404 Not Found
```json
{
  "error": "Book not found"
}
```

### 409 Conflict
```json
{
  "error": "Username already exists"
}
```

## Testing

Run the comprehensive test suite:

```bash
# Make sure the server is running first
chalice local --port 8000

# In another terminal
python test_complete_api.py
```

**Test Coverage:**
- 37 total tests
- Authentication (registration, login, tokens)
- CRUD operations (create, read, update, delete)
- Validation (all field validators)
- Error handling (malformed requests, auth failures)
- Pagination and filtering

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Books Table
```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    isbn TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Angular Frontend Integration

### Setting up CORS (if needed)

The API currently runs on `http://127.0.0.1:8000`. For Angular development:

1. Angular dev server typically runs on `http://localhost:4200`
2. You may need to configure CORS or use a proxy

### Angular Service Example

```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LibraryApiService {
  private baseUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    });
  }

  // Auth
  register(userData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/register`, userData);
  }

  login(credentials: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/login`, credentials);
  }

  // Books
  getBooks(params?: any): Observable<any> {
    return this.http.get(`${this.baseUrl}/books`, { params });
  }

  getBook(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/books/${id}`);
  }

  createBook(book: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/books`, book, {
      headers: this.getHeaders()
    });
  }

  updateBook(id: number, book: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/books/${id}`, book, {
      headers: this.getHeaders()
    });
  }

  deleteBook(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/books/${id}`, {
      headers: this.getHeaders()
    });
  }
}
```

### TypeScript Interfaces

```typescript
export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Book {
  id: number;
  title: string;
  author: string;
  year?: number;
  isbn?: string;
  created_at: string;
}

export interface PaginatedBooks {
  books: Book[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  filters: {
    author?: string;
    year?: number;
    title?: string;
  };
}

export interface AuthResponse {
  message: string;
  user: User;
  token: string;
}
```

## Environment Variables

You can override defaults using environment variables:

- `JWT_SECRET_KEY` - Secret key for JWT signing (default: "your-secret-key-change-in-production")
- `JWT_ALGORITHM` - JWT algorithm (default: "HS256")
- `JWT_TOKEN_EXPIRATION_HOURS` - Token expiration in hours (default: 24)

## Security Considerations

1. **Change JWT Secret**: Update `JWT_SECRET_KEY` in production
2. **Use HTTPS**: Deploy with SSL/TLS in production
3. **Password Storage**: Passwords are hashed using bcrypt
4. **Token Security**: Store tokens securely (HttpOnly cookies recommended)
5. **Input Validation**: All inputs are validated server-side

## Production Deployment

For AWS deployment:

```bash
chalice deploy
```

This will deploy to AWS Lambda + API Gateway.

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please create an issue in the repository.
