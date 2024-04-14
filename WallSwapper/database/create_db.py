from .tables import Base
from . import engine, Session
from .interactions import create_user, create_link

def create_db():
    with Session() as session:
        Base.metadata.reflect(engine)
        Base.metadata.drop_all(engine)
        Base.create_all(engine)

    lune = create_user("Lune", "nya")
    link = create_link(lune.token)

    print(lune)
    print(link)