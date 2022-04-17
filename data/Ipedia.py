import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Ipedia(SqlAlchemyBase):
    __tablename__ = 'Iwiki'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    think = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about_think = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    # news = orm.relation('News', back_populates='user')

    # def __repr__(self):
    #     return f'{self.name} | {self.email}'
    #
    # def set_password(self, password):
    #     self.hashed_password = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.hashed_password, password)