from os import getenv

error_code = [400, 401, 403, 404, 500, 503]
APP_SECRET_KEY = str(getenv("SERVER_SECRET_KEY"))
CSRF_EXEMPT = ["/webhook", "/health"]
redis_url = getenv("REDIS_URL", "redis://localhost:6379/0")