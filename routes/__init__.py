"""
This module is responsible for registering all the routes (blueprints) in the Flask application. It organizes the routes into groups based on their URL prefixes and provides a function to register them with the app.
@copyright: 2026 DropVault Team
@created: 2026-04-17 12:45 AM
@Author: CuSam
@license: Private / Internal Use Only
"""

from routes.auth.login import login_route
from routes.main import auth_page_route

blueprint_groups = {
    "": [auth_page_route],
    "/auth": [login_route],
}


def register_routes(app):
    try:
        for prefix, blueprints in blueprint_groups.items():
            if not isinstance(blueprints, list):
                blueprints = [blueprints]

            for bp in blueprints:
                if prefix == "":
                    app.register_blueprint(bp)
                else:
                    app.register_blueprint(bp, url_prefix=prefix)
    except Exception as e:
        print(f"[ERROR] Lỗi khi đăng ký Blueprint: {e}")
