import traceback
from datetime import UTC, datetime, timedelta
from typing import TypedDict

import jwt
from argon2 import PasswordHasher, Type
from flask import current_app

from models import User


class JWTData(TypedDict):
    uid: int
    username: str
    admin: bool
    exp: datetime


def encode_jwt(user: User):
    expires = datetime.now(tz=UTC) + timedelta(hours=1)

    return jwt.encode(
        {
            "uid": user.id,
            "username": user.username,
            "admin": user.admin,
            "exp": expires,
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )


def decode_jwt(token: str) -> JWTData | None:
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(e)
        return None


def get_jwt_data(token: str) -> tuple[dict, JWTData]:
    header = jwt.get_unverified_header(token)
    payload = jwt.decode(token, options={"verify_signature": False})
    return header, payload


def debug_jwt(token: str) -> bool | str:
    try:
        jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return True
    except Exception as e:
        # Get the traceback as a string
        return traceback.format_exc()


_ph = PasswordHasher(
    # https://www.rfc-editor.org/rfc/rfc9106.html#name-recommendations
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
    encoding="utf-8",
    type=Type.ID,
)


def hash_password(password: str) -> str:
    return _ph.hash(str(password))


def verify_password(hashed_password: str, password: str) -> bool:
    try:
        return _ph.verify(hashed_password, password)
    except Exception:
        return False
