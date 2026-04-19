"""
This module provides a function to check the strength of a password based on several criteria, including length, character variety, and common password checks. The function returns a tuple indicating whether the password is strong and an accompanying message.
@copyright: 2026 DropVault Team
@created: 2026-04-17 5:45 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import re


def check_password_strength(password: str) -> tuple[bool, str]:
    """
    check_password_strength validates the strength of a given password based on several criteria:
    - Minimum length of 8 characters
    - Maximum length of 64 characters
    - Must include at least one lowercase letter
    - Must include at least one uppercase letter
    - Must include at least one number
    Returns:
        (bool, message)
    """

    if not isinstance(password, str):
        return False, "Password must be a string"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if len(password) > 64:
        return False, "Password must not exceed 64 characters"

    # ít nhất 1 chữ thường
    if not re.search(r"[a-z]", password):
        return False, "Password must include lowercase letters"

    # ít nhất 1 chữ hoa
    if not re.search(r"[A-Z]", password):
        return False, "Password must include uppercase letters"

    # ít nhất 1 số
    if not re.search(r"[0-9]", password):
        return False, "Password must include numbers"

    # ít nhất 1 ký tự đặc biệt
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]]", password):
        return False, "Password must include special characters"

    # chặn password phổ biến
    common_passwords = {
        "12345678",
        "password",
        "123456789",
        "qwerty123",
        "admin123",
        "11111111",
        "password123",
    }

    if password.lower() in common_passwords:
        return False, "Password is too common"

    return True, "Strong password"
