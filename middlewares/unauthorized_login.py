from extensions.LoginManager import login_manager
from flask import render_template, request, jsonify


@login_manager.unauthorized_handler
def unauthorized():
    if request.accept_mimetypes.best == "application/json":
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Unauthorized access. Please log in to continue.",
                }
            ),
            401,
        )
    return render_template("errors/401.html"), 401
