from chalice import Chalice, CORSConfig
from chalicelib.database.db import init_db
from chalicelib.swagger_config import init_swagger
from chalicelib.controllers.doc_controller import register_doc_routes
from chalicelib.controllers.user_controller import register_user_routes
from chalicelib.controllers.book_controller import register_book_routes

cors_config = CORSConfig(
    allow_origin='http://localhost:4200',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Type', 'Authorization'],
    allow_credentials=True
)

app = Chalice(app_name='library-api')

init_db()

swagger_spec = init_swagger(app)

register_doc_routes(app, swagger_spec)
register_user_routes(app)
register_book_routes(app)


@app.route('/', cors=cors_config)
def index():
    return {
        'message': 'Welcome to Library API - Book Management System',
        'version': '1.0.0',
        'docs_url': '/docs'
    }
