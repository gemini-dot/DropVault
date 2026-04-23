"""
This module contains the function for user login. It verifies the user's email and password against the database and returns a success or failure message accordingly.
@copyright: 2026 DropVault Team
@created: 2026-04-16 7:46 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from extensions.database import db
from configs.argon2_config import ph
from threading import Thread
from argon2.exceptions import VerifyMismatchError


def update_password_hash(email: str, new_hash: str) -> None:
    """
    Updates the user's password hash in the database. This function is intended to be run in a separate thread to avoid blocking the main login process.
    Args:
        email (str): The email address of the user whose password hash is being updated.
        new_hash (str): The new password hash to be stored in the database.
    """
    db.users.update_one({"auth.email": email}, {"$set": {"auth.password": new_hash}})


def async_rehash(email: str, new_hash: str) -> None:
    """
    Starts a new thread to update the user's password hash in the database. This allows the login process to continue without waiting for the database update to complete.
    Args:
        email (str): The email address of the user whose password hash is being updated.
        new_hash (str): The new password hash to be stored in the database.
    """
    Thread(target=update_password_hash, args=(email, new_hash)).start()


def login_user(user_email: str, password: str) -> tuple[dict, int]:
    """
    Verifies the user's email and password against the database.
    use argon2 for password hashing and verification.
    Args:
        user_email (str): The email address of the user trying to log in.
        password (str): The plaintext password provided by the user.
    Returns:
        tuple[dict, int]: A tuple containing a dictionary with the login result and an HTTP status code.
    """

    user = db.users.find_one(
        {"auth.email": str(user_email)},
        {"_id": 0, "auth.password": 1, "auth.user_id": 1},
    )
    if not user:
        return {"success": False, "message": "User not found"}, 404

    auth_data = user.get("auth", {})
    profile_data = user.get("profile", {})
    stored_hash = auth_data.get("password")

    try:
        ph.verify(
            stored_hash, str(password)
        )  # This will raise a VerifyMismatchError if the password is incorrect, which we catch below to return an appropriate error message.

        if ph.check_needs_rehash(stored_hash):
            """
            If the stored hash needs to be rehashed (e.g., due to updated hashing parameters), we hash the password again and update the database with the new hash.
            This ensures that we are using the most secure hashing method available without forcing users to change their passwords.
            """
            new_hash = ph.hash(str(password))
            async_rehash(user_email, new_hash)

        return {
            "success": True,
            "message": "Login successful",
            "user_id": user.get("_id"),
            "username": profile_data.get("display_name", "anonymous user"),
        }, 200
    except VerifyMismatchError:
        return {"success": False, "message": "Invalid password"}, 401
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return {"success": False, "message": "An error occurred"}, 500
