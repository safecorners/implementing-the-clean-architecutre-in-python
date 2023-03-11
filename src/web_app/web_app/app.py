import flask_injector
import injector
from flask import Flask
from flask_injector import FlaskInjector

import main
from web_app.json_encoder import JSONEncoder


def create_app() -> Flask:
    app = Flask(__name__)

    app.json_decoder = JSONEncoder

    FlaskInjector(
        app,
        modules=[],
        injector=main.setup_dependency_injection(),
    )

    return app
