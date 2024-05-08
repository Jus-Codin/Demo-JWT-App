from sqlalchemy.orm import Mapped, mapped_column

from app import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    def __repr__(self):
        return f"<User {self.username}>"
