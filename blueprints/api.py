from flask import Blueprint, request

from app import db
from auth import get_user_from_token
from crypto import encode_jwt, hash_password, verify_password
from models import User

api = Blueprint("api", __name__)


@api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        return {"error": "Invalid username or password."}, 401

    user = db.session.query(User).where(User.username == username).first()
    if user is None:
        return {"error": "User does not exist."}, 401

    if verify_password(user.password, password):
        token = encode_jwt(user)
        return {"token": token}, 200
    else:
        return {"error": "Incorrect password."}, 401


@api.route("/register", methods=["POST"])
def register():
    if request.cookies.get("token") is not None:
        user = get_user_from_token(request.cookies["token"])
        if user is not None:
            return {"error": "Already logged in."}, 400

    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        return {"error": "Invalid username or password."}, 400

    user = db.session.query(User).where(User.username == username).first()
    if user is not None:
        return {"error": "Username already taken."}, 400

    try:
        password = hash_password(password)
        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return "", 201
    except Exception as e:
        print(e)
        return {"error": "Error creating user."}, 500
