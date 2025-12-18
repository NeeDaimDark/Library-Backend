from .user_controller import register_user_routes
from .book_controller import register_book_routes
from .doc_controller import register_doc_routes

__all__ = ['register_user_routes', 'register_book_routes', 'register_doc_routes']
