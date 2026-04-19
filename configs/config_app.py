"""
App Configuration
This module defines the configuration for the DropVault Flask application, including session management using Redis and response
compression settings. It sets up the necessary parameters for secure and efficient handling of user sessions and response data.
@copyright: 2026 DropVault Team
@created: 2026-04-16 12:00 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from datetime import timedelta
import redis
import os
from dotenv import load_dotenv, find_dotenv
from configs.setting import redis_url

load_dotenv(find_dotenv(), override=True)

pool = redis.ConnectionPool.from_url(
    redis_url,
    max_connections=50,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
    health_check_interval=30,
)


class Config:
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.Redis(connection_pool=pool)
    SESSION_KEY_PREFIX = "dropvault:session:"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Compression config
    COMPRESS_REGISTER = True
    COMPRESS_ALGORITHM = ["gzip"]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

    # APP
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
