"""
Login Route
This module defines the login route for the DropVault application. It handles both GET and POST requests to the /login endpoint, allowing users to access the login page and submit their credentials for authentication.
@copyright: 2026 DropVault Team
@created: 2026-04-16 12:04 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask import Blueprint
from controller.auth.login import login

login_route = Blueprint("login", __name__)


@login_route.route("/login", methods=["POST"])
def login_route_handler():
    return (
        login()
    )  # OPTIMIZE: this is a bit hacky; we should ideally refactor the controller function to be more modular and reusable without having to call it from the route handler like this, but for now this works and keeps the route handler clean and focused on routing logic.
