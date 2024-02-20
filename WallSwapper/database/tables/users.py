from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime

from . import Base


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    token = mapped_column(String(32), unique=True)
    name = mapped_column(String(32), unique=True)
    password = mapped_column(String(97))
    image = mapped_column(String(32))
    last_update = mapped_column(DateTime, default=datetime.now, nullable=False)

    links = relationship("Link", back_populates="user")

    friends = relationship("User", overlaps="friends", secondary="friendship",
        primaryjoin="User.id == Friendship.user_id", secondaryjoin="User.id == Friendship.target_id")

    controllables = relationship("User", overlaps="friends", secondary="friendship",
        primaryjoin="User.id == Friendship.target_id", secondaryjoin="User.id == Friendship.user_id")

    def __repr__(self):
        return f"User(name='{self.name}')"