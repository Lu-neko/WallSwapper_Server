from sqlalchemy import Integer, Enum, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
import enum

from . import Base


class FriendshipStates(enum.Enum):
    WAITING = 0
    BLOCKED = 1
    HAVE_TO_SUGGEST = 2
    NO_SUGGESTION = 3


class Friendship(Base):

    __tablename__ = "friendship"

    user_id = mapped_column(Integer, ForeignKey("user.id"), primary_key=True)
    target_id = mapped_column(Integer, ForeignKey("user.id"), primary_key=True)
    state = mapped_column(Enum(FriendshipStates), default=FriendshipStates.WAITING)
    image = mapped_column(String(32))

    user = relationship("User", overlaps="controllables,friends", foreign_keys=[user_id])
    target = relationship("User", overlaps="controllables,friends", foreign_keys=[target_id])

    def __repr__(self):
        return f"Friendship('{self.user}' and '{self.target}')"