"""
This module defines the route for the authentication page (the "gate" page where users can choose to log in or sign up). It includes a rate limit to prevent abuse of the accounts page, and it checks if the user is already logged in to redirect them to the dashboard instead of showing the gate page again. The actual login and signup functionality will be handled in separate routes and controllers, but this serves as the entry point for users accessing the authentication system.
@copyright: 2026 DropVault Team
@created: 2026-04-17 12:45 AM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask import Blueprint, render_template, session, redirect, url_for
from middlewares.rate_limit import rate_limit

auth_page_route = Blueprint("auth_page", __name__)


@auth_page_route.route("/accounts", methods=["GET"])
@rate_limit(
    max_requests=10, window_seconds=60
)  # Limit to 10 requests per minute per IP address to prevent abuse of the accounts page; adjust as needed based on expected traffic and usage patterns.
def auth_page():
    if "user_id" in session:
        return redirect(
            url_for("dashboard")
        )  # TODO: redirect to dashboard instead of rendering the gate page if the user is already logged in; this is just a placeholder for now until we implement the dashboard route and template.
    return render_template("auth/gate.html")
