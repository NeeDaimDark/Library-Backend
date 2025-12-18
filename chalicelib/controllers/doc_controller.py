from chalice import Response
from chalicelib.templates.swagger_ui import get_swagger_ui_html


def register_doc_routes(app, swagger_spec):

    @app.route('/docs', methods=['GET'])
    def swagger_ui():
        html = get_swagger_ui_html()
        return Response(body=html, status_code=200, headers={'Content-Type': 'text/html; charset=utf-8'})

    @app.route('/swagger.json', methods=['GET'])
    def swagger_json():
        return swagger_spec

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        return Response(body='', status_code=204)
