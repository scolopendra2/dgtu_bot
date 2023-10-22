import sqlalchemy
from sqlalchemy.orm import relationship

from loader import Base


class Passport(Base):
    __tablename__ = 'passports'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')
    )
    full_name = sqlalchemy.Column(sqlalchemy.String)
    series_and_number = sqlalchemy.Column(sqlalchemy.String)

    user = relationship('User', back_populates='passport')
