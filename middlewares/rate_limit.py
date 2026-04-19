"""
Rate Limiting Middleware
This module implements a rate limiting middleware using Redis sorted sets and Lua scripting for atomic operations. It provides a decorator that can be applied to Flask route handlers to enforce rate limits based on client IP address and endpoint.
@copyright: 2026 DropVault Team
@created: 2026-04-16 12:00 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

import time
import uuid
from functools import wraps
from flask import request, jsonify, make_response
from extensions.redis_client import r

# =========================
# Lua Script
# =========================
LUA_SCRIPT = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local max_requests = tonumber(ARGV[3])
local member = ARGV[4]

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

local count = redis.call('ZCARD', key)

if count >= max_requests then
    return count
end

redis.call('ZADD', key, now, member)
redis.call('EXPIRE', key, window)

return count + 1
"""

# Lazy singleton
_rate_limit_script = None


def get_rate_limit_script():
    """
    Load the Lua script into Redis and return a callable that executes the script.
    This function uses lazy loading to ensure the script is only loaded once and reused for subsequent calls.
    """
    global _rate_limit_script
    if _rate_limit_script is None:
        _rate_limit_script = r.register_script(
            LUA_SCRIPT
        )  # NOTE: this will load the script into Redis and return a callable that can be used to execute the script with the appropriate keys and arguments
    return _rate_limit_script


# =========================
# Decorator
# =========================
def rate_limit(max_requests: int, window_seconds: int):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            from utils.network import get_client_ip

            identifier = (
                get_client_ip()
            )  # HACK: use IP address as identifier; in production, consider using a more robust identifier (e.g., user ID or API key) if available
            endpoint = request.endpoint or "unknown"

            key = f"rate_limit:{identifier}:{endpoint}"
            now = time.time()
            member = f"{now}-{uuid.uuid4().hex}"

            try:
                script = get_rate_limit_script()
                count = script(
                    keys=[key], args=[now, window_seconds, max_requests, member]
                )
            except Exception:
                # fail-open
                return f(*args, **kwargs)

            if count > max_requests:
                return jsonify({"success": False, "message": "Too many requests"}), 429

            response = make_response(f(*args, **kwargs))

            response.headers["X-RateLimit-Limit"] = max_requests
            response.headers["X-RateLimit-Remaining"] = max(0, max_requests - count)
            response.headers["X-RateLimit-Reset"] = int(now + window_seconds)

            return response

        return wrapped

    return decorator
