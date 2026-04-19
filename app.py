"""
Main Application Entry Point
This module initializes the Flask application, configures middleware, registers routes, and sets up error handling. It also includes security measures such as CSRF protection and rate limiting.
@copyright: 2026 DropVault Team
@created: 2026-04-16 12:00 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import sys
import io
from flask import Flask, render_template, request
from configs.setting import error_code as error_codes
from configs.config_app import Config
from configs.setting import APP_SECRET_KEY
from routes import register_routes
from flask_cors import CORS
from configs.sentry import init_sentry
from flask_session import Session
from flask_compress import Compress
from utils.security.csrf import validate_csrf, generate_csrf_token
from configs.setting import CSRF_EXEMPT
from extensions.limiter import limiter
from extensions.database import db


def create_app():

    app = Flask(__name__)

    limiter.init_app(app)

    app.config.from_object(Config)

    app.secret_key = APP_SECRET_KEY

    app.config.update(
        SESSION_COOKIE_DOMAIN=".vault-storage.me",
        SESSION_COOKIE_NAME="vault-storage-session",
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE="Lax",  # HACK: With the previous project, Lax could cause server errors; this needs to be considered before use.
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_PATH="/",
    )

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

    @app.before_request
    def csrf_protect():

        generate_csrf_token()  # Ensure that a CSRF token is generated for each request and stored in the session, so it can be validated for state-changing requests (POST, PUT, PATCH, DELETE). This helps protect against CSRF attacks by ensuring that the request is coming from a trusted source (i.e., the user's browser with a valid session) and not from a malicious third-party site. The token should be included in the request headers or form data for validation in the validate_csrf() function.

        if request.endpoint and request.endpoint in CSRF_EXEMPT:
            return
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            validate_csrf()

    @app.route("/")
    def main():
        return render_template("index.html")

    return app
