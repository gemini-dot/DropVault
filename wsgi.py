"""
This module serves as the entry point for the DropVault web application. It initializes the Flask application by calling the `create_app` function from the `app` package and starts the development server. The server is configured to listen on all available interfaces (
@copyright: 2026 DropVault Team
@created: 2026-04-17 5:20 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
