"""
This module provides functions for managing user sessions in a Flask application. It allows you to set session data for the user, which can be used to store information about the user's session, such as their user ID, email, or other preferences. The session data is stored on the server side and is associated with a unique session ID that is sent to the client as a cookie. This allows the application to maintain state across multiple requests from the same user.
@copyright: 2026 DropVault Team
@created: 2026-04-16 10:05 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask import session
from typing import Any


def set_session(
    session_id: str, user_id: str, permanent=True, **session_data: Any
) -> None:
    """
    Sets the session data for the user. This function can be used to store any relevant information about the user's session, such as their user ID, email, or other preferences.
    Args:
        session_id (str): The unique identifier for the session.
        user_id (str): The unique identifier for the user.
        permanent (bool): Whether the session should be permanent.
        **session_data: Arbitrary keyword arguments representing the session data to be stored.
    """

    session.pop("user_id", None)
    session.pop("session_id", None)

    session["session_id"] = session_id
    session["user_id"] = user_id

    session.permanent = permanent  # Make the session permanent so it will last until the user closes their browser or the session expires

    for key, value in session_data.items():
        if key not in ("user_id", "session_id"):
            session[key] = value
