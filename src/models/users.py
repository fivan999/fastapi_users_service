import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String

from src.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    password_updated_at = Column(
        type_=TIMESTAMP(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
        - datetime.timedelta(minutes=10),
    )
    is_active = Column(Boolean, default=True)
