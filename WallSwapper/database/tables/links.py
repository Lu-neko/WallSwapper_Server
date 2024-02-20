from sqlalchemy import Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime

from . import Base


class Link(Base):
    __tablename__ = "link"

    url = mapped_column(String(16), primary_key=True)
    uses = mapped_column(SmallInteger)
    expiration = mapped_column(DateTime, nullable=False)
    last_use = mapped_column(DateTime, default=datetime.now, nullable=False)

    user_id = mapped_column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="links")

    def __repr__(self):
        return f"Link(url='/{self.url}')"