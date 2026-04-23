"""
This module defines the User model for the DropVault application, which is used for authentication and user management.
@copyright: 2026 DropVault Team
@created: 2026-04-17 1:30 AM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask_login import UserMixin
from bson import ObjectId
from bson.errors import InvalidId


class User(UserMixin):
    """User model for authentication and user management."""

    def __init__(self, id, username, email, is_active=True, role="user"):
        self.id = id
        self.username = username
        self.email = email
        self._is_active = is_active
        self.role = role

    def get_id(self) -> str:
        """Return the unique identifier of the user as a string."""
        return str(self.id)

    def is_active(self) -> bool:
        """Return whether the user account is active."""
        return self._is_active

    @staticmethod
    def get_by_id(user_id: str) -> "User" | None:
        from configs.database import db

        try:
            data = db.users.find_one(
                {"_id": ObjectId(user_id)}, {"_id": 1, "auth": 1, "profile": 1}
            )
        except InvalidId:
            return None
        except Exception as e:
            print(f"An error occurred while fetching user by ID: {e}")
            return None

        if not data:
            return None

        auth = data.get("auth", {})
        profile = data.get("profile", {})

        return User(
            id=data.get("_id"),
            username=profile.get("display_name_normalized", "anonymous user"),
            email=auth.get("email"),
            is_active=(auth.get("status") == "active"),
            role=auth.get("role", "user"),
        )
