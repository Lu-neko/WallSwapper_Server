from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import DB_PASS, DB_URL, DB_PORT, DB_NAME
from .tables import Base, User, Link, Friendship

engine = create_engine(f"postgresql+psycopg2://postgres:{DB_PASS}@{DB_URL}:{DB_PORT}/{DB_NAME}")

Session = sessionmaker(engine)