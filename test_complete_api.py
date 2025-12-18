import requests
import json
import time
from typing import Dict, Any, Optional, Tuple

BASE_URL = 'http://127.0.0.1:8000'

class APITester:
    def __init__(self):
        self.token: Optional[str] = None
        self.user_id: Optional[int] = None
        self.book_ids: list = []
        self.passed = 0
        self.failed = 0
        self.test_username: Optional[str] = None
        self.test_password: Optional[str] = None

    def print_result(self, test_name: str, passed: bool, message: str = '') -> None:
        status = '✓ PASS' if passed else '✗ FAIL'
        print(f'{status}: {test_name}')
        if message:
            print(f'  └─ {message}')

    def print_section(self, title: str) -> None:
        print(f'\n{"="*60}')
        print(f'{title}')
        print(f'{"="*60}')

    def track_result(self, passed: bool) -> None:
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def test_register_valid_user(self) -> bool:
        """Test: Register with valid credentials"""
        self.print_section('AUTHENTICATION - Registration Tests')
        
        timestamp = int(time.time() * 1000)
        payload = {
            'username': f'testuser{timestamp}',
            'email': f'test{timestamp}@example.com',
            'password': 'SecurePass123!'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        passed = response.status_code == 201
        self.print_result('Register valid user', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        
        if passed:
            self.user_id = response.json().get('user_id')
            self.test_username = payload['username']
            self.test_password = payload['password']
        return passed

    def test_register_duplicate_username(self) -> bool:
        """Test: Register with duplicate username (should fail)"""
        payload = {
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'AnotherPass123!'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        passed = response.status_code == 409
        self.print_result('Register duplicate username', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_register_invalid_email(self) -> bool:
        """Test: Register with invalid email (should fail)"""
        payload = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password': 'SecurePass123!'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        passed = response.status_code == 400
        self.print_result('Register invalid email', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_register_weak_password(self) -> bool:
        """Test: Register with weak password (should fail)"""
        payload = {
            'username': 'anotheruser',
            'email': 'anotheruser@example.com',
            'password': '123'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        passed = response.status_code == 400
        self.print_result('Register weak password', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_register_missing_fields(self) -> bool:
        """Test: Register with missing required fields"""
        payload = {
            'username': 'incompleteuser',
            'email': 'incomplete@example.com'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        passed = response.status_code == 400
        self.print_result('Register missing fields', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_login_valid_credentials(self) -> bool:
        """Test: Login with valid credentials"""
        self.print_section('AUTHENTICATION - Login & Token Tests')
        
        if not self.test_username or not self.test_password:
            self.print_result('Login valid credentials', False, 'No test credentials available')
            self.track_result(False)
            return False
        
        payload = {
            'username': self.test_username,
            'password': self.test_password
        }
        
        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        passed = response.status_code == 200
        self.print_result('Login valid credentials', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        
        if passed:
            data = response.json()
            self.token = data.get('token')
            token_exists = self.token is not None and len(self.token) > 0
            self.print_result('Token received', token_exists, f'Token length: {len(self.token) if self.token else 0}')
            self.track_result(token_exists)
        
        return passed

    def test_login_invalid_username(self) -> bool:
        """Test: Login with invalid username"""
        payload = {
            'username': 'nonexistent',
            'password': 'SomePass123!'
        }
        
        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        passed = response.status_code == 401
        self.print_result('Login invalid username', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_login_invalid_password(self) -> bool:
        """Test: Login with invalid password"""
        payload = {
            'username': 'testuser',
            'password': 'WrongPassword123!'
        }
        
        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        passed = response.status_code == 401
        self.print_result('Login invalid password', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_login_missing_fields(self) -> bool:
        """Test: Login with missing fields"""
        payload = {
            'username': 'testuser'
        }
        
        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        passed = response.status_code == 400
        self.print_result('Login missing fields', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_create_book_with_token(self) -> bool:
        """Test: Create book with valid token"""
        self.print_section('BOOKS - CRUD Operations')
        
        if not self.token:
            self.print_result('Create book with token', False, 'No token available')
            self.track_result(False)
            return False
        
        payload = {
            'title': 'Clean Code',
            'author': 'Robert C. Martin',
            'year': 2008,
            'isbn': '978-0-13-235088-4'
        }
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(f'{BASE_URL}/books', json=payload, headers=headers)
        passed = response.status_code == 201
        self.print_result('Create book with token', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        
        if passed:
            self.book_ids.append(response.json().get('book_id'))
        
        return passed

    def test_create_book_without_token(self) -> bool:
        """Test: Create book without token (should fail)"""
        payload = {
            'title': 'Design Patterns',
            'author': 'Gang of Four',
            'year': 1994,
            'isbn': '978-0-201-63361-0'
        }
        
        response = requests.post(f'{BASE_URL}/books', json=payload)
        passed = response.status_code == 401
        self.print_result('Create book without token', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_create_book_invalid_token(self) -> bool:
        """Test: Create book with invalid token"""
        payload = {
            'title': 'Python Crash Course',
            'author': 'Eric Matthes',
            'year': 2019,
            'isbn': '978-1-492-03966-7'
        }
        
        headers = {'Authorization': 'Bearer invalid.token.here'}
        response = requests.post(f'{BASE_URL}/books', json=payload, headers=headers)
        passed = response.status_code == 401
        self.print_result('Create book invalid token', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_create_book_missing_required_fields(self) -> bool:
        """Test: Create book with missing required fields"""
        payload = {
            'title': 'Incomplete Book',
        }
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(f'{BASE_URL}/books', json=payload, headers=headers)
        passed = response.status_code == 400
        self.print_result('Create book missing fields', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_create_book_invalid_year(self) -> bool:
        """Test: Create book with invalid year"""
        payload = {
            'title': 'Future Book',
            'author': 'Someone',
            'year': 2999,
            'isbn': '978-0-123456-78-9'
        }
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(f'{BASE_URL}/books', json=payload, headers=headers)
        passed = response.status_code == 400
        self.print_result('Create book invalid year', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_create_book_invalid_isbn(self) -> bool:
        """Test: Create book with invalid ISBN"""
        payload = {
            'title': 'Bad ISBN Book',
            'author': 'Someone',
            'year': 2020,
            'isbn': 'invalid-isbn'
        }
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(f'{BASE_URL}/books', json=payload, headers=headers)
        passed = response.status_code == 400
        self.print_result('Create book invalid ISBN', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_get_all_books(self) -> bool:
        """Test: Get all books"""
        response = requests.get(f'{BASE_URL}/books')
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_books = 'books' in data and isinstance(data['books'], list)
            has_pagination = 'total' in data and 'page' in data and 'per_page' in data
            passed = has_books and has_pagination
            message = f'Status: {response.status_code}, Books: {len(data.get("books", []))}, Total: {data.get("total", 0)}'
        else:
            message = f'Status: {response.status_code}'
        
        self.print_result('Get all books', passed, message)
        self.track_result(passed)
        return passed

    def test_get_books_with_pagination(self) -> bool:
        """Test: Get books with pagination parameters"""
        params = {'page': 1, 'per_page': 5}
        response = requests.get(f'{BASE_URL}/books', params=params)
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_correct_params = data.get('page') == 1 and data.get('per_page') == 5
            passed = has_correct_params
            message = f'Page: {data.get("page")}, Per Page: {data.get("per_page")}'
        else:
            message = f'Status: {response.status_code}'
        
        self.print_result('Get books with pagination', passed, message)
        self.track_result(passed)
        return passed

    def test_get_books_with_title_filter(self) -> bool:
        """Test: Get books filtered by title"""
        params = {'title': 'Clean'}
        response = requests.get(f'{BASE_URL}/books', params=params)
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            message = f'Books found: {len(data.get("books", []))}'
        else:
            message = f'Status: {response.status_code}'
        
        self.print_result('Get books filter by title', passed, message)
        self.track_result(passed)
        return passed

    def test_get_books_with_author_filter(self) -> bool:
        """Test: Get books filtered by author"""
        params = {'author': 'Robert'}
        response = requests.get(f'{BASE_URL}/books', params=params)
        passed = response.status_code == 200
        self.print_result('Get books filter by author', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_get_books_with_year_filter(self) -> bool:
        """Test: Get books filtered by year"""
        params = {'year': 2008}
        response = requests.get(f'{BASE_URL}/books', params=params)
        passed = response.status_code == 200
        self.print_result('Get books filter by year', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_get_book_by_id(self) -> bool:
        """Test: Get book by ID"""
        if not self.book_ids:
            self.print_result('Get book by ID', False, 'No book IDs available')
            self.track_result(False)
            return False
        
        book_id = self.book_ids[0]
        response = requests.get(f'{BASE_URL}/books/{book_id}')
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            book = data.get('book', {})
            has_id = book.get('id') is not None
            message = f'Book ID: {book.get("id")}, Title: {book.get("title")}'
            passed = has_id
        else:
            message = f'Status: {response.status_code}'
        
        self.print_result('Get book by ID', passed, message)
        self.track_result(passed)
        return passed

    def test_get_nonexistent_book(self) -> bool:
        """Test: Get nonexistent book (should fail)"""
        response = requests.get(f'{BASE_URL}/books/99999')
        passed = response.status_code == 404
        self.print_result('Get nonexistent book', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_update_book_with_token(self) -> bool:
        """Test: Update book with valid token"""
        self.print_section('BOOKS - Update Operations')
        
        if not self.book_ids or not self.token:
            self.print_result('Update book with token', False, 'No book IDs or token available')
            self.track_result(False)
            return False
        
        book_id = self.book_ids[0]
        payload = {
            'title': 'Clean Code - Updated Edition',
            'author': 'Robert C. Martin',
            'year': 2009
        }
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.put(f'{BASE_URL}/books/{book_id}', json=payload, headers=headers)
        passed = response.status_code == 200
        self.print_result('Update book with token', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_update_book_without_token(self) -> bool:
        """Test: Update book without token (should fail)"""
        if not self.book_ids:
            self.print_result('Update book without token', False, 'No book IDs available')
            self.track_result(False)
            return False
        
        book_id = self.book_ids[0]
        payload = {'title': 'Attempted Update'}
        response = requests.put(f'{BASE_URL}/books/{book_id}', json=payload)
        passed = response.status_code == 401
        self.print_result('Update book without token', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_update_nonexistent_book(self) -> bool:
        """Test: Update nonexistent book"""
        payload = {'title': 'Nonexistent Book'}
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.put(f'{BASE_URL}/books/99999', json=payload, headers=headers)
        passed = response.status_code == 404
        self.print_result('Update nonexistent book', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_update_book_invalid_year(self) -> bool:
        """Test: Update book with invalid year"""
        if not self.book_ids:
            self.print_result('Update book invalid year', False, 'No book IDs available')
            self.track_result(False)
            return False
        
        book_id = self.book_ids[0]
        payload = {'year': 3000}
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.put(f'{BASE_URL}/books/{book_id}', json=payload, headers=headers)
        passed = response.status_code == 400
        self.print_result('Update book invalid year', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_delete_book_without_token(self) -> bool:
        """Test: Delete book without token (should fail)"""
        self.print_section('BOOKS - Delete Operations')
        
        if not self.book_ids:
            self.print_result('Delete book without token', False, 'No book IDs available')
            self.track_result(False)
            return False
        
        book_id = self.book_ids[0]
        response = requests.delete(f'{BASE_URL}/books/{book_id}')
        passed = response.status_code == 401
        self.print_result('Delete book without token', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_delete_nonexistent_book(self) -> bool:
        """Test: Delete nonexistent book"""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.delete(f'{BASE_URL}/books/99999', headers=headers)
        passed = response.status_code == 404
        self.print_result('Delete nonexistent book', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_delete_book_with_token(self) -> bool:
        """Test: Delete book with valid token"""
        if not self.book_ids or not self.token:
            self.print_result('Delete book with token', False, 'No book IDs or token available')
            self.track_result(False)
            return False
        
        book_id = self.book_ids[0]
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.delete(f'{BASE_URL}/books/{book_id}', headers=headers)
        passed = response.status_code == 200
        self.print_result('Delete book with token', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        
        if passed:
            self.book_ids.remove(book_id)
        
        return passed

    def test_validator_empty_username(self) -> bool:
        """Test: Validator - Empty username"""
        self.print_section('VALIDATORS - Field Validation')
        
        payload = {
            'username': '',
            'email': 'validator@example.com',
            'password': 'ValidPass123!'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        passed = response.status_code == 400
        self.print_result('Validator empty username', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_validator_empty_email(self) -> bool:
        """Test: Validator - Empty email"""
        payload = {
            'username': 'validatoruser',
            'email': '',
            'password': 'ValidPass123!'
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        passed = response.status_code == 400
        self.print_result('Validator empty email', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_validator_empty_title(self) -> bool:
        """Test: Validator - Empty book title"""
        if not self.token:
            self.print_result('Validator empty title', False, 'No token available')
            self.track_result(False)
            return False
        
        payload = {
            'title': '',
            'author': 'Some Author',
            'year': 2020
        }
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(f'{BASE_URL}/books', json=payload, headers=headers)
        passed = response.status_code == 400
        self.print_result('Validator empty title', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_validator_empty_author(self) -> bool:
        """Test: Validator - Empty book author"""
        if not self.token:
            self.print_result('Validator empty author', False, 'No token available')
            self.track_result(False)
            return False
        
        payload = {
            'title': 'Some Title',
            'author': '',
            'year': 2020
        }
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(f'{BASE_URL}/books', json=payload, headers=headers)
        passed = response.status_code == 400
        self.print_result('Validator empty author', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_error_handling_malformed_json(self) -> bool:
        """Test: Error handling - Malformed JSON"""
        self.print_section('ERROR HANDLING - Invalid Requests')
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{BASE_URL}/auth/login', data='{invalid json}', headers=headers)
        passed = response.status_code in [400, 415]
        self.print_result('Error handling malformed JSON', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_error_handling_invalid_method(self) -> bool:
        """Test: Error handling - Invalid HTTP method"""
        response = requests.patch(f'{BASE_URL}/auth/register', json={})
        passed = response.status_code == 405
        self.print_result('Error handling invalid method', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def test_error_handling_nonexistent_endpoint(self) -> bool:
        """Test: Error handling - Nonexistent endpoint"""
        response = requests.get(f'{BASE_URL}/nonexistent/endpoint')
        passed = response.status_code in [403, 404]
        self.print_result('Error handling nonexistent endpoint', passed, f'Status: {response.status_code}')
        self.track_result(passed)
        return passed

    def run_all_tests(self) -> None:
        """Run all tests"""
        print('\n' + '='*60)
        print('LIBRARY API - COMPREHENSIVE TEST SUITE')
        print('='*60)

        self.test_register_valid_user()
        self.test_register_duplicate_username()
        self.test_register_invalid_email()
        self.test_register_weak_password()
        self.test_register_missing_fields()

        self.test_login_valid_credentials()
        self.test_login_invalid_username()
        self.test_login_invalid_password()
        self.test_login_missing_fields()

        self.test_create_book_with_token()
        self.test_create_book_without_token()
        self.test_create_book_invalid_token()
        self.test_create_book_missing_required_fields()
        self.test_create_book_invalid_year()
        self.test_create_book_invalid_isbn()

        self.test_get_all_books()
        self.test_get_books_with_pagination()
        self.test_get_books_with_title_filter()
        self.test_get_books_with_author_filter()
        self.test_get_books_with_year_filter()
        self.test_get_book_by_id()
        self.test_get_nonexistent_book()

        self.test_update_book_with_token()
        self.test_update_book_without_token()
        self.test_update_nonexistent_book()
        self.test_update_book_invalid_year()

        self.test_delete_book_without_token()
        self.test_delete_nonexistent_book()
        self.test_delete_book_with_token()

        self.test_validator_empty_username()
        self.test_validator_empty_email()
        self.test_validator_empty_title()
        self.test_validator_empty_author()

        self.test_error_handling_malformed_json()
        self.test_error_handling_invalid_method()
        self.test_error_handling_nonexistent_endpoint()

        self.print_summary()

    def print_summary(self) -> None:
        """Print test summary"""
        self.print_section('TEST SUMMARY')
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f'Total Tests: {total}')
        print(f'Passed: {self.passed} ✓')
        print(f'Failed: {self.failed} ✗')
        print(f'Success Rate: {percentage:.1f}%')
        print(f'{"="*60}\n')


if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()
