from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    @classmethod
    def create_all(cls, engine):
        Base.metadata.create_all(engine)


from .users import User
from .links import Link
from .friendship import Friendship, FriendshipStates