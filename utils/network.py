"""
file: network.py
this module is used to get the client's IP address from the request headers. It checks for the 'CF-Connecting-IP' header (used by Cloudflare), then the 'X-Forwarded-For' header (used by proxies), and finally falls back to the remote address of the request if neither header is present.
@copyright: 2026 DropVault Team
@created: 2026-04-16 10:30 PM
@Author: CuSam
@license: Private / Internal Use Only
"""

from flask import request


def get_client_ip() -> str:
    # Check for Cloudflare's connecting IP header
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip
    # Check for X-Forwarded-For header (used by proxies)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # fallback
    return request.remote_addr or "0.0.0.0"
