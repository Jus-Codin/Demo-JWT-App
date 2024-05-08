import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    db_url = os.environ.get("DATABASE_URL", f"sqlite:///database.db")
    secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

    print(f" * Database URL: {db_url}")
    print(f" * Secret Key: {secret_key}")

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    from blueprints.api import api
    from blueprints.web import web

    app.register_blueprint(web, url_prefix="/")
    app.register_blueprint(api, url_prefix="/api")

    app.add_url_rule("/", endpoint="index")

    from crypto import hash_password
    from models import User

    with app.app_context():
        db.drop_all()
        db.create_all()

        password = hash_password("password")

        db.session.execute(
            insert(User),
            [
                {"username": "admin", "password": password, "admin": True},
                {"username": "user", "password": password, "admin": False},
            ],
        )
        db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
