"""
File: controller/auth/login.py
This module contains the controller function for user login. It receives the login request, extracts the email and password, and calls the login service to verify the credentials. It then returns the appropriate response based on the result of the login attempt.
@copyright: 2026 DropVault Team
@created: 2026-04-16 8:45 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import datetime
from services.auth.login import login_user
from flask import request, jsonify, url_for
from services.auth.session import set_session
from utils.network import get_client_ip
from user_agents import parse
import secrets
from middlewares.rate_limit import rate_limit


@rate_limit(
    max_requests=5, window_seconds=60
)  # Limit to 5 login attempts per minute per IP address to prevent brute-force attacks
def login() -> tuple[dict, int] | str:

    if request.method == "POST":

        data = request.get_json() or request.form

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"success": False, "message": "Email and password are required"}, 400

        result, status_code = login_user(
            email, password
        )  # NOTE: login_user should return a tuple of (result_dict, status_code)

        if status_code == 200:
            # TODO: log user login activity (e.g., log the login time, IP address, and user agent for security monitoring)
            ua_string = request.headers.get("User-Agent", "")
            user_agent = parse(ua_string)

            now = datetime.datetime.now(datetime.timezone.utc)
            session_id = secrets.token_urlsafe(32)

            # TODO: save session data to database or in-memory store (e.g., Redis) for session management and tracking
            set_session(
                session_id=session_id,
                user_id=result.get("user_id"),
                ip_address=get_client_ip(),
                browser=user_agent.browser.family,
                os=user_agent.os.family,
                created_at=now,
                last_active=now,
                expires_at=now + datetime.timedelta(days=7),
                raw_ua=ua_string,
            )

            return jsonify(
                {"redirect": url_for("dashboard")}
            )  # TODO: redirect to dashboard
        return {
            "success": False,
            "message": "Incorrect username or password",
        }, status_code  # TODO: handle error messages properly in the frontend
