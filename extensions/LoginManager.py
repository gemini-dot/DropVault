"""
LoginManager.py
This module initializes the LoginManager for handling user authentication and session management in the DropVault application.
@license: Private / Internal Use Only
@copyright: 2026 DropVault Team
@created: 2026-04-17 1:00 AM
@Author: CuSam
"""

from flask_login import LoginManager

# Initialize the LoginManager for handling user authentication and session management in the DropVault application. This will be used to manage user login states, handle unauthorized access, and integrate with the User model for authentication purposes. The LoginManager will be configured in the main application setup to ensure that it works seamlessly with the Flask app and the defined user model.
login_manager = LoginManager()
