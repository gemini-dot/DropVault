"""
This module defines the register_user function, which handles the registration of new users in the DropVault application. It validates the provided email, password, and username, checks for existing users with the same email, hashes the password securely using Argon2, and stores the new user's information in the database. The function returns a success message and user ID upon successful registration or an appropriate error message if validation fails or an exception occurs.
@copyright: 2026 DropVault Team
@created: 2026-04-16 7:50 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from extensions.database import db
import datetime
from validators.auth.valid_email import is_valid_email
from validators.auth.check_password_strength import check_password_strength
from validators.auth.valid_username_length import is_valid_username_length
from configs.argon2_config import ph
from utils.text.normalization import remove_accents
from extensions.response import response
from pymongo.errors import DuplicateKeyError


def register_user(email: str, password: str, username: str) -> tuple[dict, int]:
    """
    Registers a new user in the database with the provided email and password hash.
    Args:
        email (str): The email address of the user to be registered.
        password (str): The password provided by the user.
        username (str): The username for the new user.
    Returns:
        tuple[dict, int]: A tuple containing a dictionary with the registration result and an HTTP status code.
    """

    email = (
        email.strip().lower()
    )  # Normalize email by trimming whitespace and converting to lowercase
    username = username.strip()

    # Validate email format
    if not is_valid_email(email):
        return response(success=False, message="Invalid email format"), 400

    # Validate username length
    is_valid, msg = is_valid_username_length(username)

    if not is_valid:
        return response(success=False, message=msg), 400

    # Check password strength
    is_strong, message = check_password_strength(password)
    if not is_strong:
        return response(success=False, message=message), 400
    try:
        if db.users.find_one({"auth.email": email}):
            return response(success=False, message="Email already registered"), 400

        password_hash = ph.hash(
            password
        )  # Hash the password using Argon2 for secure storage

        now = datetime.datetime.now(datetime.timezone.utc)

        user_id = db.users.insert_one(
            {
                "auth": {
                    "email": email,
                    "password": password_hash,
                    "role": "user",  # Default role is 'user', can be updated later by an admin
                    "status": "active",  # User status can be 'active', 'inactive', 'banned', etc.
                },
                "profile": {
                    "display_name": username,  # Default display name is the provided username
                    "display_name_normalized": remove_accents(
                        username
                    ),  # Normalized display name for search and sorting
                    "avatar_url": None,  # Placeholder for user avatar URL, can be updated later
                    "created_at": now,  # Timestamp for when the user was created
                    "updated_at": now,  # Timestamp for when the user profile was last updated
                },
                "storage": {
                    "root_folder_id": None,  # Placeholder for the ID of the user's root folder, can be set after folder creation
                    "total_space_bytes": 1073741824,  # Default total storage space allocated to the user (1 GB)
                    "used_space_bytes": 0,
                    "plan": "free",
                },
                "settings": {
                    "theme": "light",  # Default theme is 'light', can be updated by the user
                    "language": "en",  # Default language is English, can be updated by the user
                    "two_factor_auth": False,  # NOTE: Two-factor authentication is disabled by default, can be enabled by the user for added security
                },
            }
        ).inserted_id

        return response(success=True, message="User registered successfully"), 201
    except DuplicateKeyError:
        return response(False, "Email already exists"), 400
    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return (
            response(success=False, message="An error occurred during registration"),
            500,
        )
