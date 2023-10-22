import sqlalchemy

from loader import Base


class Train(Base):
    __tablename__ = 'trains'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    train_name = sqlalchemy.Column(sqlalchemy.String)
    product_ids = sqlalchemy.Column(sqlalchemy.String)
