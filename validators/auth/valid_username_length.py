"""
Validates the length of a username.
@copyright: 2026 DropVault Team
@created: 2026-04-17 6:00 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import re


def is_valid_username_length(username: str, min_len: int = 3, max_len: int = 30):
    username = username.strip()

    if not username:
        return False, "Username cannot be empty"

    if len(username) < min_len:
        return False, f"Username too short (min {min_len})"

    if len(username) > max_len:
        return False, f"Username too long (max {max_len})"

    # chặn ký tự nguy hiểm cơ bản
    if not re.match(r"^[a-zA-Z0-9_ ]+$", username):
        return False, "Username contains invalid characters"

    return True, "OK"
