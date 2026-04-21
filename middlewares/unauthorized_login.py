"""
This module defines a custom unauthorized handler for the Flask-Login extension. When a user attempts to access a protected route without being authenticated, this handler will be invoked. It checks the client's request to determine if they prefer a JSON response or an HTML response and returns the appropriate response accordingly.
@license: Private / Internal Use Only
@copyright: 2026 DropVault Team
@created: 2026-04-17 2:30 AM
@Author: CuSam
"""


from extensions.LoginManager import login_manager
from flask import render_template, request, jsonify


@login_manager.unauthorized_handler
def unauthorized():
    wants_json = (
        request.is_json
        or request.accept_mimetypes["application/json"]
        >= request.accept_mimetypes["text/html"]
    )

    if wants_json:
        return jsonify(
            {
                "success": False,
                "message": "Unauthorized access. Please log in to continue.",
            }
        ), 401

    return render_template("errors/401.html"), 401
