import json
from flask import Flask
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(__name__)

    # Load config.py
    app.config.from_pyfile('config.py')

    # jsonify HTTP errors
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    # Import blueprints
    from app.blueprints.api.routes import api
    from app.blueprints.main.routes import main

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')

    return app