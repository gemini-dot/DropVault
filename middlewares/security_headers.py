"""
This module sets security headers for the Flask application to enhance security against common web vulnerabilities.
@license: Private / Internal Use Only
@copyright: 2026 DropVault Team
@created: 2026-04-17 2:00 AM
@Author: CuSam
"""

def register_security_headers(app):
    @app.after_request
    def set_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://res.cloudinary.com; "
            "media-src https://res.cloudinary.com; "
            "object-src 'none'; "
            "frame-ancestors 'none';"
        )
        return response
