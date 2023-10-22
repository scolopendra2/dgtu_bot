import sqlalchemy
from sqlalchemy.orm import relationship

from loader import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')
    )
    number_train = sqlalchemy.Column(sqlalchemy.String)
    number_val = sqlalchemy.Column(sqlalchemy.String)
    number_place = sqlalchemy.Column(sqlalchemy.String)

    user = relationship('User', back_populates='ticket')
