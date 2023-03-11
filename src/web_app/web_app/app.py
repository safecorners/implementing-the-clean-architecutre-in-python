import os
from typing import Optional

import flask_injector
import injector
from flask import Flask, Response
from flask_injector import FlaskInjector

from main import bootstrap_app
from web_app.json_encoder import JSONEncoder
from web_app.security import setup as security_setup


def create_app(settings_override: Optional[dict] = None) -> Flask:
    if settings_override is None:
        settings_override = {}

    app = Flask(__name__)

    app.json_decoder = JSONEncoder

    app.config["DEBUG"] = True
    # Generate a key using secrets.token_urlsafe()
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "vcKIB0yxmI8pZEA6l8rb03obj5S5Anigk3dpDZ3yWYk"
    )
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
        "SECURITY_PASSWORD_SALT", "115344098186654686680422612806219269083"
    )
    # Specifies whether registration email is sent. Defaults to True.
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False
    # Specifies if Flask-Security should create a user registration endpoint.
    # The URL for this endpoint is specified by the SECURITY_REGISTER_URL(/register)
    # configuration option. Defaults to False.
    app.config["SECURITY_REGISTERABLE"] = True
    # Disable CSRF Protection
    app.config["WTF_CSRF_ENABLED"] = False

    for key, value in settings_override.items():
        app.config[key] = value

    app_context = bootstrap_app()
    FlaskInjector(app, modules=[], injector=app_context.injector)
    app.injector = app_context.injector

    security_setup(app)

    return app
