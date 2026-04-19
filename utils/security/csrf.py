import secrets
from flask import session, request, abort
from os import getenv

def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def validate_csrf():

    if getenv("FLASK_ENV") == "development":
        return

    token = request.headers.get("X-CSRF-Token")
    session_token = session.get("csrf_token")

    if not token or not session_token or token != session_token:
        abort(403)
