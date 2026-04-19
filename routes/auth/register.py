from controller.auth.register import register
from flask import Blueprint

register_route = Blueprint("register", __name__)

register_route.route("/register", methods=["POST"])(register)