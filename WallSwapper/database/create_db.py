from .tables import Base
from . import engine, Session

def create_db():
    with Session() as session:
        Base.metadata.reflect(engine)
        Base.metadata.drop_all(engine)
        Base.create_all(engine)