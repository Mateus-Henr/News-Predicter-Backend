from flask import Flask
from flask_cors import CORS

from app.routes import news_routes


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(news_routes)

    return app
