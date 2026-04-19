"""
This module provides a standardized response format for API endpoints in the DropVault application.
@copyright: 2026 DropVault Team
@created: 2026-04-17 5:45 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask import jsonify


def response(success=True, message="", data=None):
    return jsonify({"success": success, "message": message, "data": data})
