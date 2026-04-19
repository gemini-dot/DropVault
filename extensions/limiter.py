"""
This module initializes the Flask-Limiter extension for rate limiting in the application. It configures the limiter to use Redis as the storage backend and sets default limits for requests per day and per hour. The limiter is then integrated into the Flask application to help prevent abuse and ensure fair usage of the API endpoints.
@copyright: 2026 DropVault Team
@created: 2026-04-17 5:15 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from configs.setting import redis_url

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_url,
    storage_options={"ssl_cert_reqs": None},
    default_limits=["200 per day", "50 per hour"],
)
