from .tables import User, Link, Friendship, FriendshipStates
from . import Session

from secrets import token_urlsafe
from argon2 import PasswordHasher
from datetime import datetime, timedelta
import secrets

ph = PasswordHasher(time_cost=1)

def create_user(name, password):
    with Session() as session:
        if session.query(User).filter_by(name=name).first():
            return None

        token = secrets.token_urlsafe(24)
        while session.query(User).filter_by(token=token).first():
            token = secrets.token_urlsafe(24)

        try:
            hash = ph.hash(password)
        except:
            return False

        user = User(name=name, password=hash, token=token)
        session.add(user)
        session.commit()
        return user

def connect_user(name, password):
    with Session() as session:
        user = session.query(User).filter_by(name=name).first()

    if not user:
        return None

    try:
        ph.verify(user.password, password)
    except:
        return False

    return user

def get_user(token):
    with Session() as session:
        user = session.query(User).filter_by(token=token).first()

    if not user:
        return None

    return user

def url_set_image(url, image):
    with Session() as session:
        link = session.query(Link).filter_by(url=url).first()

        if not link:
            return False

        if link.expiration < datetime.now():
            session.delete(link)
            return False

        if link.uses:
            link.uses-=1
            session.refresh()
            if link.uses < 0:
                session.delete(link)
                return False

        link.last_use = datetime.now()
        link.user.image = image

        session.commit()

        return True

def friend_set_image(token, target_id, image):
    with Session() as session:
        user = session.query(User).filter_by(token=token).first()

        if not user:
            return False

        friendship = session.query(Friendship).filter_by(target=user, user_id=target_id).first()

        if not friendship:
            return False

        if friendship.state == FriendshipStates.HAVE_TO_SUGGEST:
            friendship.image = image
            session.commit()
            return True
        elif friendship.state == FriendshipStates.NO_SUGGESTION:
            friendship.user.image = image
            session.commit()
            return True
        else:
            return False

def create_link(token, uses=None, expiration=None):
    with Session() as session:
        user = session.query(User).filter_by(token=token).first()

        if not user:
            return None

        if len(user.links) > 99:
            return False

        url = secrets.token_urlsafe(12)
        while session.query(Link).filter_by(url=url).first():
            url = secrets.token_urlsafe(12)

        if not expiration:
            expiration = datetime.now() + timedelta(days=60)

        link = Link(url=url, uses=uses, expiration=expiration, user=user)

        session.add(link)
        session.commit()

        session.expunge(link)
        return link

def delete_link(token, url):
    with Session() as session:
        user = session.query(User).filter_by(token=token).first()

        if not user:
            return False

        link = session.query(Link).filter_by(url=url).first()

        if not link:
            return False

        if not link.user == user:
            return False

        session.delete(link)
        session.commit()
        return True

