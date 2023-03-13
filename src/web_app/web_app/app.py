import os
from typing import Optional

import injector
from flask import Flask, Response, request
from flask_injector import FlaskInjector
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from main import bootstrap_app
from main.modules import RequestScope
from web_app.blueprints.auctions import AuctionsWeb, auctions_blueprint
from web_app.json_encoder import JSONEncoder
from web_app.security import setup as security_setup


def create_app(settings_override: Optional[dict] = None) -> Flask:
    if settings_override is None:
        settings_override = {}

    app = Flask(__name__)

    # app.json_decoder = JSONEncoder

    app.register_blueprint(auctions_blueprint, url_prefix="/auctions")

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
    # Disable pre-request CSRF
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    # Check csrf for session and http auth (but not token)
    # app.config["SECURITY_CSRF_PROTECT_MECHANISMS"] = ["basic", "session"]

    for key, value in settings_override.items():
        app.config[key] = value

    app_context = bootstrap_app()
    FlaskInjector(app, modules=[AuctionsWeb()], injector=app_context.injector)
    app.injector = app_context.injector  # type: ignore

    @app.before_request
    def transaction_start() -> None:
        app_context.injector.get(RequestScope).enter()
        request.connection = app_context.injector.get(Connection)  # type: ignore
        request.tx = request.connection.begin()  # type: ignore
        request.session = app_context.injector.get(Session)  # type: ignore

    @app.after_request
    def transaction_end(response: Response) -> Response:
        scope = app_context.injector.get(RequestScope)
        try:
            if hasattr(request, "tx") and response.status_code < 400:
                request.tx.commit()  # type: ignore
        finally:
            scope.exit()

        return response

    security_setup(app)

    return app
