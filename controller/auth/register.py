from services.auth.register import register_user
from flask import request
from middlewares.rate_limit import rate_limit
from validators.auth.register_schema import RegisterSchema
from extensions.response import response


@rate_limit(max_requests=10, window_seconds=60)
def register() -> tuple:
    data = request.get_json(silent=True) or request.form

    if not data:
        return response(False, "Invalid or missing JSON"), 400

    schema = RegisterSchema(
        email=data.get("email"),
        password=data.get("password"),
        username=data.get("username"),
    )
    ok, msg = schema.validate()
    if not ok:
        return response(False, msg), 400

    result, status_code = register_user(
        schema.email, schema.password, schema.username
    )  # NOTE: register_user should return a tuple of (result_dict, status_code)

    return (
        response(
            result.get("success", False), result.get("message", ""), result.get("data")
        ),
        status_code,
    )
