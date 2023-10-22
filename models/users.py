import sqlalchemy

from loader import Base
from sqlalchemy.orm import relationship

from .passports import Passport


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    tg_user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    passport = relationship('Passport', back_populates='user')
