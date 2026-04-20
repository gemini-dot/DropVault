"""
Main Application Entry Point
This module initializes the Flask application, configures middleware, registers routes, and sets up error handling. It also includes security measures such as CSRF protection and rate limiting.
@copyright: 2026 DropVault Team
@created: 2026-04-16 12:00 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask import Flask, render_template
from configs.setting import error_code as error_codes
from configs.config_app import Config
from configs.setting import APP_SECRET_KEY
from routes import register_routes
from flask_cors import CORS
from configs.sentry import init_sentry
from flask_session import Session
from flask_compress import Compress
from extensions.limiter import limiter
from flask_wtf import CSRFProtect
from middlewares.security_headers import register_security_headers

csrf = CSRFProtect()


def create_app():

    app = Flask(__name__)

    limiter.init_app(app)
    csrf.init_app(app)
    register_security_headers(app)

    app.config.from_object(Config)

    app.secret_key = APP_SECRET_KEY

    app.config.update(
        SESSION_COOKIE_NAME="vault-storage-session",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_PATH="/",
    )

    if app.debug:
        app.config["SESSION_COOKIE_DOMAIN"] = None
        app.config["SESSION_COOKIE_SECURE"] = False
        app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    else:
        app.config["SESSION_COOKIE_DOMAIN"] = ".vault-storage.me"
        app.config["SESSION_COOKIE_SECURE"] = True
        app.config["SESSION_COOKIE_SAMESITE"] = "None"  # cross-site

    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "https://www.vault-storage.me",
            "https://vault-storage.me",
            "https://dashboard.vault-storage.me",
            "https://api.vault-storage.me",
            "https://dropvault-uxeo.onrender.com",
            # TODO: add more allowed origins as needed, and consider using environment variables for better flexibility in different deployment environments
            # TODO: Use render.com to test before deploying to Azure.
        ],
    )

    init_sentry()
    Session(app)
    Compress(app)

    register_routes(
        app
    )  # Register all routes (blueprints) with the Flask app using the function defined in routes/__init__.py

    def handle_error(e):
        code = getattr(e, "code", 500)

        return render_template(f"errors/{code}.html"), code

    for code in error_codes:
        try:
            app.register_error_handler(code, handle_error)
        except Exception as e:
            print(f"Error registering handler for {code}: {e}")

    @app.route("/")
    def main():
        return render_template("index.html")

    return app
