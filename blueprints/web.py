from flask import Blueprint, redirect, render_template, request, send_file, url_for

from auth import get_user_from_token, is_admin, is_authenticated
from crypto import debug_jwt, get_jwt_data
from models import User

web = Blueprint("web", __name__)


@web.route("/", methods=["GET"])
def index():
    token = request.cookies.get("token")
    if token is None:
        user = None
        header = None
        payload = None
    else:
        header, payload = get_jwt_data(token)
        user = get_user_from_token(token)
        if user is None:
            return redirect(url_for("web.invalid_token"))

    return render_template(
        "index.html", user=user, token=token, header=header, payload=payload
    )


@web.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_file("static/img/console.png")


@web.route("/logout", methods=["GET"])
def logout():
    response = redirect(url_for("web.index"))
    response.set_cookie("token", "", expires=0)
    return response


@web.route("/user_only", methods=["GET"])
@is_authenticated
def users_only(user: User):
    token = request.cookies["token"]
    header, payload = get_jwt_data(token)
    return render_template(
        "user_only.html", user=user, token=token, header=header, payload=payload
    )


@web.route("/admin_only", methods=["GET"])
@is_admin
def admin_only(user: User):
    token = request.cookies["token"]
    header, payload = get_jwt_data(token)
    return render_template(
        "admin_only.html", user=user, token=token, header=header, payload=payload
    )


@web.route("/invalid_token", methods=["GET"])
def invalid_token():
    token = request.cookies.get("token")
    if token:
        if get_user_from_token(token) is not None:
            return redirect(url_for("web.index"))
        header, payload = get_jwt_data(token)
        error = debug_jwt(token)
        return render_template(
            "invalid_token.html", header=header, payload=payload, error=error
        )
    else:
        # This should never happen, redirect to index
        print("How did you get here?")
        return redirect(url_for("web.index"))


def handle_error(message: str, status_code: int):
    token = request.cookies.get("token")
    if token is None:
        user = None
        header = None
        payload = None
    else:
        header, payload = get_jwt_data(token)
        user = get_user_from_token(token)
        if user is None:
            response = redirect(url_for("web.index"))
            response.set_cookie("token", "", expires=0)
            return response

    return (
        render_template(
            "error.html",
            message=message,
            status_code=status_code,
            user=user,
            token=token,
            header=header,
            payload=payload,
        ),
        status_code,
    )


@web.app_errorhandler(401)
def unauthorized(e):
    return handle_error("You are not authorized to view this page.", 401)


@web.app_errorhandler(403)
def forbidden(e):
    return handle_error("You are not authorized to view this page.", 403)


@web.app_errorhandler(404)
def not_found(e):
    return handle_error("The page you are looking for does not exist.", 404)
