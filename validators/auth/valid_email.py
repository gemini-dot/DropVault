"""
This module provides a function to validate email addresses using a regular expression pattern. The function checks if the input is a string, trims any leading or trailing whitespace, and then matches it against a standard email format. It returns True if the email is valid and False otherwise.
@copyright: 2026 DropVault Team
@created: 2026-04-17 5:30 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import re

EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9](?:[a-zA-Z0-9._%+-]{0,62}[a-zA-Z0-9])?"
    r"@[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+$"
)


def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False

    email = email.strip().lower()
    return bool(EMAIL_PATTERN.match(email))
