from functools import wraps

from flask import abort, redirect, request, url_for

from app import db
from crypto import decode_jwt
from models import User


def get_user_from_token(token: str) -> User | None:
    data = decode_jwt(token)
    if data is None:
        return None

    return db.session.query(User).get(data["uid"])


def is_authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")

        if token is None:
            return abort(401)

        user = get_user_from_token(token)

        if user is None:
            return redirect(url_for("web.invalid_token"))
        else:
            return f(user, *args, **kwargs)

    return wrapper


def is_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")

        if token is None:
            return abort(401)

        data = decode_jwt(token)
        if data is None:
            return redirect(url_for("web.invalid_token"))

        user = db.session.query(User).get(data["uid"])

        if user is None:
            return redirect(url_for("web.invalid_token"))
        elif not data["admin"]:
            return abort(403)
        else:
            return f(user, *args, **kwargs)

    return wrapper
